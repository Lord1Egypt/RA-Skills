import DiscordAdapter from './adapters/discord.js';
import fs from 'fs/promises';
import path from 'path';

class DiscordIngestionRunner {
  constructor(ingestModule, options = {}) {
    this.ingestModule = ingestModule; // ClawTextIngester instance
    this.options = options;
    this.stats = {
      totalFetched: 0,
      totalIngested: 0,
      totalDeduplicated: 0,
      failed: [],
      startTime: null,
      endTime: null,
    };
  }

  /**
   * Main entry point: ingest Discord forum autonomously
   * Returns: { success, summary, stats }
   */
  async ingestForumAutonomous(config) {
    const {
      forumId,
      mode = 'batch',              // 'full' | 'batch' | 'posts-only'
      batchSize = 50,
      concurrency = 3,
      skipEmbeds = true,
      skipAttachments = true,
      preserveHierarchy = true,
      dedupStrategy = 'strict',    // 'strict' | 'lenient' | 'skip'
      token = process.env.DISCORD_TOKEN,
      outputPath = null,           // Save intermediate results
      onProgress = null,
    } = config;

    this.stats.startTime = Date.now();
    let adapter = null;

    try {
      // Initialize adapter
      adapter = new DiscordAdapter({
        token,
        includeEmbeds: !skipEmbeds,
        includeAttachments: !skipAttachments,
        concurrency,
        batchSize,
        progressCallback: onProgress,
      });

      await adapter.authenticate();

      // Understand forum scope
      const forumInfo = await adapter.describeForumStructure(forumId);
      console.log(`📊 Forum: "${forumInfo.name}" | Posts: ${forumInfo.postCount} | Est. Messages: ${forumInfo.estimatedMessageCount}`);

      // Choose mode based on forum size
      let finalMode = mode;
      if (forumInfo.postCount >= adapter.autoBatchThreshold && mode === 'full') {
        console.log(`⚠️  Forum too large for 'full' mode (${forumInfo.postCount} posts). Switching to 'batch'.`);
        finalMode = 'batch';
      }

      // Execute based on mode
      let result;
      if (finalMode === 'full') {
        result = await this._ingestForumFull(adapter, forumId, forumInfo, preserveHierarchy, dedupStrategy, outputPath);
      } else if (finalMode === 'batch') {
        result = await this._ingestForumBatch(adapter, forumId, forumInfo, batchSize, preserveHierarchy, dedupStrategy, outputPath);
      } else if (finalMode === 'posts-only') {
        result = await this._ingestForumPostsOnly(adapter, forumId, forumInfo, preserveHierarchy, dedupStrategy, outputPath);
      }

      this.stats.endTime = Date.now();
      return {
        success: true,
        summary: result.summary,
        stats: this.stats,
      };
    } catch (error) {
      this.stats.endTime = Date.now();
      console.error('❌ Forum ingestion failed:', error.message);
      return {
        success: false,
        error: error.message,
        stats: this.stats,
      };
    } finally {
      if (adapter) await adapter.disconnect();
    }
  }

  /**
   * Full mode: fetch entire forum at once
   */
  async _ingestForumFull(adapter, forumId, forumInfo, preserveHierarchy, dedupStrategy, outputPath) {
    console.log('📥 Fetching entire forum...');
    
    const { forumMetadata, records, relationshipMap } = await adapter.fetchForumCompletely(forumId);
    
    console.log(`✅ Fetched ${records.length} messages from ${forumMetadata.totalPosts} posts`);
    this.stats.totalFetched = records.length;

    // Save intermediate if requested
    if (outputPath) {
      await this._saveIntermediate(outputPath, { forumMetadata, records, relationshipMap });
    }

    // Ingest to ClawText
    const ingestResult = await this._ingestBatch(records, {
      source: 'discord',
      sourceType: 'forum',
      forumId,
      forumName: forumMetadata.forumName,
      preserveHierarchy,
      relationshipMap: preserveHierarchy ? relationshipMap : null,
    }, dedupStrategy);

    this.stats.totalIngested = ingestResult.ingestedCount;
    this.stats.totalDeduplicated = ingestResult.duplicateSkipped;

    return {
      summary: {
        mode: 'full',
        forum: forumMetadata.forumName,
        totalPosts: forumMetadata.totalPosts,
        totalMessages: forumMetadata.totalMessages,
        ingestedMessages: ingestResult.ingestedCount,
        deduplicatedMessages: ingestResult.duplicateSkipped,
        hierarchyPreserved: preserveHierarchy,
        duration: `${((this.stats.endTime - this.stats.startTime) / 1000).toFixed(2)}s`,
      },
    };
  }

  /**
   * Batch mode: fetch and ingest in streaming fashion
   */
  async _ingestForumBatch(adapter, forumId, forumInfo, batchSize, preserveHierarchy, dedupStrategy, outputPath) {
    console.log(`📥 Fetching forum in batches (size: ${batchSize})...`);

    let totalMessages = 0;
    let batchNumber = 0;
    const relationshipMap = {};

    for await (const batch of adapter.fetchForumInBatches(forumId, { batchSize })) {
      batchNumber++;
      totalMessages += batch.records.length;

      // Merge relationship maps
      Object.assign(relationshipMap, batch.relationshipMap);

      console.log(`  Batch ${batchNumber}: ${batch.records.length} messages`);

      // Ingest this batch
      const ingestResult = await this._ingestBatch(batch.records, {
        source: 'discord',
        sourceType: 'forum',
        forumId,
        forumName: batch.forumName,
        preserveHierarchy,
        relationshipMap: preserveHierarchy ? batch.relationshipMap : null,
      }, dedupStrategy);

      this.stats.totalIngested += ingestResult.ingestedCount;
      this.stats.totalDeduplicated += ingestResult.duplicateSkipped;
    }

    this.stats.totalFetched = totalMessages;

    // Save final relationship map if preserving
    if (outputPath && preserveHierarchy) {
      await this._saveIntermediate(outputPath, { relationshipMap });
    }

    return {
      summary: {
        mode: 'batch',
        forum: forumInfo.name,
        totalPosts: forumInfo.postCount,
        totalMessages: totalMessages,
        totalBatches: batchNumber,
        ingestedMessages: this.stats.totalIngested,
        deduplicatedMessages: this.stats.totalDeduplicated,
        hierarchyPreserved: preserveHierarchy,
        duration: `${((this.stats.endTime - this.stats.startTime) / 1000).toFixed(2)}s`,
      },
    };
  }

  /**
   * Posts-only mode: fetch only root post messages
   */
  async _ingestForumPostsOnly(adapter, forumId, forumInfo, preserveHierarchy, dedupStrategy, outputPath) {
    console.log('📥 Fetching forum post roots only...');

    const hierarchy = await adapter.fetchForumHierarchy(forumId);
    const records = hierarchy.map(post => ({
      id: `post_root_${post.postId}`,
      source: 'discord',
      sourceType: 'forum_post_root',
      content: post.postName, // Use post name as content
      author: post.authorId,
      timestamp: post.createdAt,
      forumHierarchy: {
        forumId,
        postId: post.postId,
        postName: post.postName,
        depth: 0,
      },
      metadata: {
        messageCount: post.messageCount,
        tags: post.tags,
        archived: post.archived,
      },
    }));

    console.log(`✅ Fetched ${records.length} post roots`);
    this.stats.totalFetched = records.length;

    // Save intermediate if requested
    if (outputPath) {
      await this._saveIntermediate(outputPath, { records, postCount: records.length });
    }

    // Ingest to ClawText
    const ingestResult = await this._ingestBatch(records, {
      source: 'discord',
      sourceType: 'forum',
      forumId,
      forumName: forumInfo.name,
      preserveHierarchy: false, // Posts-only doesn't need hierarchy
    }, dedupStrategy);

    this.stats.totalIngested = ingestResult.ingestedCount;
    this.stats.totalDeduplicated = ingestResult.duplicateSkipped;

    return {
      summary: {
        mode: 'posts-only',
        forum: forumInfo.name,
        totalPosts: records.length,
        ingestedMessages: ingestResult.ingestedCount,
        deduplicatedMessages: ingestResult.duplicateSkipped,
        duration: `${((this.stats.endTime - this.stats.startTime) / 1000).toFixed(2)}s`,
      },
    };
  }

  /**
   * Internal: Ingest a batch to ClawText
   */
  async _ingestBatch(records, metadata, dedupStrategy) {
    try {
      return await this.ingestModule.fromJSON(
        records,
        metadata,
        { checkDedupe: dedupStrategy !== 'skip' }
      );
    } catch (error) {
      console.error(`  ❌ Batch ingest failed: ${error.message}`);
      this.stats.failed.push({
        error: error.message,
        recordCount: records.length,
      });
      return { ingestedCount: 0, duplicateSkipped: 0 };
    }
  }

  /**
   * Internal: Save intermediate results to disk
   */
  async _saveIntermediate(filePath, data) {
    try {
      await fs.mkdir(path.dirname(filePath), { recursive: true });
      await fs.writeFile(filePath, JSON.stringify(data, null, 2));
      console.log(`💾 Saved intermediate results to ${filePath}`);
    } catch (error) {
      console.warn(`⚠️  Could not save intermediate results: ${error.message}`);
    }
  }
}

export default DiscordIngestionRunner;
