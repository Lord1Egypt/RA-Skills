#!/usr/bin/env node

/**
 * AI Content Repurposer - CLI
 * Command-line interface for content transformation
 */

const { Command } = require('commander');
const fs = require('fs');
const path = require('path');
const ContentConverter = require('../src/converter');

const program = new Command();

program
  .name('ai-content-repurposer')
  .description('Transform long-form content into multiple formats')
  .version('1.0.0');

// YouTube to Short-form command
program
  .command('youtube-to-shorts')
  .description('Convert YouTube video to TikTok/Shorts/Reels script')
  .argument('<transcript>', 'Path to transcript file or text')
  .option('-p, --platform <platform>', 'Target platform (tiktok, shorts, reels)', 'tiktok')
  .option('-o, --output <file>', 'Output file path')
  .action(async (transcript, options) => {
    const converter = new ContentConverter();
    
    let content;
    if (fs.existsSync(transcript)) {
      content = fs.readFileSync(transcript, 'utf-8');
    } else {
      content = transcript;
    }

    console.log(`\n🎬 Converting to ${options.platform} script...`);
    
    try {
      const result = await converter.youtubeToShortForm(content, options.platform);
      
      if (options.output) {
        fs.writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(`✅ Saved to ${options.output}`);
      } else {
        console.log('\n📝 Script:');
        console.log(`Title: ${result.title}`);
        console.log(`Hook: ${result.hook}`);
        console.log('\nBody:');
        result.body.forEach((point, i) => console.log(`  ${i + 1}. ${point}`));
        console.log(`\nCTA: ${result.cta}`);
        console.log(`Hashtags: ${result.hashtags.join(' ')}`);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Blog to Twitter thread command
program
  .command('blog-to-twitter')
  .description('Convert blog post to Twitter thread')
  .argument('<url-or-file>', 'Blog URL or file path')
  .option('-n, --tweets <number>', 'Number of tweets', '7')
  .option('-o, --output <file>', 'Output file path')
  .action(async (source, options) => {
    const converter = new ContentConverter();
    
    let content;
    if (source.startsWith('http')) {
      console.log('📥 Fetching blog content...');
      content = await converter.fetchBlogContent(source);
    } else if (fs.existsSync(source)) {
      content = fs.readFileSync(source, 'utf-8');
    } else {
      content = source;
    }

    console.log(`\n🐦 Creating Twitter thread (${options.tweets} tweets)...`);
    
    try {
      const result = await converter.blogToTwitterThread(content, parseInt(options.tweets));
      
      if (options.output) {
        fs.writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(`✅ Saved to ${options.output}`);
      } else {
        console.log('\n🧵 Thread:');
        result.tweets.forEach(tweet => {
          console.log(`\n${tweet.number}/${result.tweets.length}: ${tweet.text}`);
        });
        console.log(`\nHashtags: ${result.hashtags.join(' ')}`);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Blog to LinkedIn command
program
  .command('blog-to-linkedin')
  .description('Convert blog post to LinkedIn post')
  .argument('<url-or-file>', 'Blog URL or file path')
  .option('-t, --tone <tone>', 'Tone (thought-leadership, educational, story)', 'thought-leadership')
  .option('-o, --output <file>', 'Output file path')
  .action(async (source, options) => {
    const converter = new ContentConverter();
    
    let content;
    if (source.startsWith('http')) {
      console.log('📥 Fetching blog content...');
      content = await converter.fetchBlogContent(source);
    } else if (fs.existsSync(source)) {
      content = fs.readFileSync(source, 'utf-8');
    } else {
      content = source;
    }

    console.log(`\n💼 Creating LinkedIn post (${options.tone})...`);
    
    try {
      const result = await converter.blogToLinkedIn(content, options.tone);
      
      if (options.output) {
        fs.writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(`✅ Saved to ${options.output}`);
      } else {
        console.log('\n📄 LinkedIn Post:');
        console.log(`${result.hook}\n`);
        console.log(`${result.body}\n`);
        console.log(`💡 ${result.insight}\n`);
        console.log(`❓ ${result.question}\n`);
        console.log(`Hashtags: ${result.hashtags.join(' ')}`);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Podcast to transcript command
program
  .command('podcast-to-transcript')
  .description('Format podcast transcript with chapters')
  .argument('<transcript>', 'Path to transcript file')
  .option('--no-timestamps', 'Disable timestamps')
  .option('--speakers', 'Add speaker labels')
  .option('-o, --output <file>', 'Output file path')
  .action(async (transcriptFile, options) => {
    const converter = new ContentConverter();
    
    if (!fs.existsSync(transcriptFile)) {
      console.error('❌ Transcript file not found');
      process.exit(1);
    }

    const content = fs.readFileSync(transcriptFile, 'utf-8');
    console.log('\n🎙️ Formatting podcast transcript...');
    
    try {
      const result = await converter.podcastToTranscript(content, {
        includeTimestamps: options.timestamps !== false,
        speakerLabels: options.speakers || false
      });
      
      if (options.output) {
        fs.writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(`✅ Saved to ${options.output}`);
      } else {
        console.log('\n📑 Chapters:');
        result.chapters.forEach(chapter => {
          console.log(`\n[${chapter.timestamp}] ${chapter.title}`);
          console.log(chapter.content.substring(0, 200) + '...');
        });
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Podcast to summary command
program
  .command('podcast-to-summary')
  .description('Generate podcast summary and quote cards')
  .argument('<transcript>', 'Path to transcript file')
  .option('-o, --output <file>', 'Output file path')
  .action(async (transcriptFile, options) => {
    const converter = new ContentConverter();
    
    if (!fs.existsSync(transcriptFile)) {
      console.error('❌ Transcript file not found');
      process.exit(1);
    }

    const content = fs.readFileSync(transcriptFile, 'utf-8');
    console.log('\n📝 Generating summary and quotes...');
    
    try {
      const result = await converter.podcastToSummary(content);
      
      if (options.output) {
        fs.writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(`✅ Saved to ${options.output}`);
      } else {
        console.log('\n📊 Summary:');
        console.log(result.summary);
        
        console.log('\n💡 Key Takeaways:');
        result.takeaways.forEach((takeaway, i) => console.log(`  ${i + 1}. ${takeaway}`));
        
        console.log('\n💬 Top Quotes:');
        result.quotes.slice(0, 5).forEach(quote => {
          console.log(`  "${quote.text}"`);
        });
        
        console.log('\n📱 Social Post Ideas:');
        result.socialPosts.forEach((post, i) => {
          console.log(`  ${i + 1}. [${post.platform}] ${post.content.substring(0, 100)}...`);
        });
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Batch conversion command
program
  .command('batch')
  .description('Batch convert multiple content pieces')
  .argument('<config>', 'Path to batch config JSON file')
  .option('-o, --output-dir <dir>', 'Output directory', './output')
  .action(async (configFile, options) => {
    if (!fs.existsSync(configFile)) {
      console.error('❌ Config file not found');
      process.exit(1);
    }

    const config = JSON.parse(fs.readFileSync(configFile, 'utf-8'));
    const converter = new ContentConverter();
    
    // Create output directory
    if (!fs.existsSync(options.outputDir)) {
      fs.mkdirSync(options.outputDir, { recursive: true });
    }

    console.log(`\n🚀 Batch processing ${config.jobs.length} jobs...\n`);

    for (const [index, job] of config.jobs.entries()) {
      console.log(`[${index + 1}/${config.jobs.length}] Processing: ${job.name}`);
      
      try {
        let result;
        const outputFile = path.join(options.outputDir, `${job.name}.json`);
        
        switch (job.type) {
          case 'youtube-to-shorts':
            result = await converter.youtubeToShortForm(job.content, job.platform || 'tiktok');
            break;
          case 'blog-to-twitter':
            result = await converter.blogToTwitterThread(job.content, job.tweetCount || 7);
            break;
          case 'blog-to-linkedin':
            result = await converter.blogToLinkedIn(job.content, job.tone || 'thought-leadership');
            break;
          case 'podcast-to-summary':
            result = await converter.podcastToSummary(job.content);
            break;
          default:
            console.log(`  ⚠️  Unknown job type: ${job.type}`);
            continue;
        }
        
        fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
        console.log(`  ✅ Saved to ${outputFile}`);
      } catch (error) {
        console.log(`  ❌ Error: ${error.message}`);
      }
    }

    console.log('\n🎉 Batch processing complete!');
  });

// Interactive mode
program
  .command('interactive')
  .description('Run in interactive mode')
  .action(() => {
    console.log('\n🎭 AI Content Repurposer - Interactive Mode');
    console.log('Type "help" for commands, "exit" to quit\n');
    
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const askQuestion = (query) => new Promise(resolve => readline.question(query, resolve));

    (async () => {
      while (true) {
        const type = await askQuestion('Conversion type (youtube/blog/podcast/exit): ');
        
        if (type.toLowerCase() === 'exit') break;

        if (type === 'youtube') {
          const platform = await askQuestion('Platform (tiktok/shorts/reels): ');
          const transcript = await askQuestion('Paste transcript (or file path): ');
          // Process...
        } else if (type === 'blog') {
          const target = await askQuestion('Target (twitter/linkedin): ');
          const url = await askQuestion('Blog URL or file path: ');
          // Process...
        } else if (type === 'podcast') {
          const output = await askQuestion('Output (transcript/summary/both): ');
          const file = await askQuestion('Transcript file path: ');
          // Process...
        }
      }

      readline.close();
    })();
  });

program.parse();
