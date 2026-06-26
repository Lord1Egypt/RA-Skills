#!/usr/bin/env node
/**
 * ForgeObsidianBrain - Main Entry Point
 * CLI interface for the Obsidian Brain skill
 */

const { discoverVault } = require('./vault/discover');
const { getAllSettings, ensureBrainFolders } = require('./vault/config');
const { readNote, createNote, updateNote, deleteNote, listNotes, noteExists } = require('./note/crud');
const { searchNotes, searchNotesFuzzy, searchNotesRegex } = require('./search/search');
const { runSync, analyzeSync } = require('./sync');
const fs = require('fs');
const path = require('path');

const VERSION = '1.0.0';

function showHelp() {
  console.log(`
ForgeObsidianBrain v${VERSION}

Usage: brain.js <command> [options]

Core Commands:
  discover                          Auto-discover vault location
  config                            Show vault configuration
  init                              Initialize Brain folder structure
  sync                              Bidirectional sync with memory folder

Note CRUD Commands:
  read <note-path>                  Read a note
  create <note-path> [content]      Create a new note
  update <note-path> [content]      Update an existing note
  delete <note-path>                Delete a note
  list [folder]                     List notes in folder (default: root)
  search <query>                    Search notes for query (case-insensitive by default)
                                    --fuzzy        Use fuzzy matching (typo-tolerant)
                                    --regex        Use regex pattern matching
                                    --case-sensitive  Force case-sensitive search
  exists <note-path>                Check if note exists

Capture Commands:
  capture thought <text>            Capture a fleeting thought to Brain/Thoughts/
  capture research --url <url>      Save research with URL to Brain/Research/
                  --title <title>
  capture conversation              Log conversation to Brain/Conversations/
            --source <telegram|discord>
            --id <id> [--text <text>]

Resurface Commands:
  resurface topic <query>           Search vault, return top 5 matches
  resurface stale --days <n>        Find notes not modified in N days

Options:
  --vault <path>                    Specify vault path (overrides auto-discovery)
  --frontmatter '<json>'            Add frontmatter as JSON (create/update)
  --merge                           Merge frontmatter instead of replace (update)
  --overwrite                       Overwrite existing note (create)
  --limit <n>                       Limit results (default: 5)
  --dry-run                         Preview only for sync

Environment Variables:
  OBSIDIAN_VAULT                    Default vault path

Examples:
  # Auto-discover vault
  brain.js discover

  # Capture a thought
  brain.js capture thought "I should refactor the auth module"

  # Save research
  brain.js capture research --url https://example.com --title "System Design Tips"

  # Find stale notes
  brain.js resurface stale --days 30
`);
}

function parseArgs(args) {
  const options = {
    vault: null,
    frontmatter: null,
    merge: false,
    overwrite: false,
    limit: 5,
    dryRun: false,
    url: null,
    title: null,
    source: null,
    id: null,
    text: null,
    days: 30,
    fuzzy: false,
    regex: false,
    caseSensitive: false,
  };
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--vault') {
      options.vault = args[++i];
    } else if (arg === '--frontmatter') {
      const fm = args[++i];
      try {
        options.frontmatter = JSON.parse(fm);
      } catch (e) {
        console.error(`Invalid frontmatter JSON: ${fm}`);
        process.exit(1);
      }
    } else if (arg === '--merge') {
      options.merge = true;
    } else if (arg === '--overwrite') {
      options.overwrite = true;
    } else if (arg === '--limit') {
      const parsed = parseInt(args[++i], 10);
      options.limit = isNaN(parsed) ? 5 : parsed;
    } else if (arg === '--dry-run') {
      options.dryRun = true;
    } else if (arg === '--url') {
      options.url = args[++i];
    } else if (arg === '--title') {
      options.title = args[++i];
    } else if (arg === '--source') {
      options.source = args[++i];
    } else if (arg === '--id') {
      options.id = args[++i];
    } else if (arg === '--text') {
      options.text = args[++i];
    } else if (arg === '--days') {
      const parsed = parseInt(args[++i], 10);
      options.days = isNaN(parsed) ? 30 : parsed;
    } else if (arg === '--fuzzy') {
      options.fuzzy = true;
    } else if (arg === '--regex') {
      options.regex = true;
    } else if (arg === '--case-sensitive') {
      options.caseSensitive = true;
    } else if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    } else if (arg === '--version' || arg === '-v') {
      console.log(VERSION);
      process.exit(0);
    } else if (!arg.startsWith('--')) {
      positional.push(arg);
    }
  }

  return { options, positional };
}

function getVaultPath(options) {
  if (options.vault) {
    return options.vault;
  }

  if (process.env.OBSIDIAN_VAULT) {
    return process.env.OBSIDIAN_VAULT;
  }

  const discovery = discoverVault();
  if (discovery.success) {
    return discovery.path;
  }

  return null;
}

function getTimestamp() {
  return new Date().toISOString();
}

function generateNoteId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    showHelp();
    process.exit(0);
  }

  const { options, positional } = parseArgs(args);
  const command = positional[0];

  if (!command) {
    showHelp();
    process.exit(1);
  }

  // Handle commands that don't need vault
  if (command === 'discover') {
    const preferred = options.vault || process.env.OBSIDIAN_VAULT;
    const result = discoverVault({ preferred });
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
    return;
  }

  // All other commands need a vault
  const vaultPath = getVaultPath(options);

  if (!vaultPath) {
    console.error('Error: Could not find vault. Please specify with --vault or set OBSIDIAN_VAULT');
    process.exit(1);
  }

  switch (command) {
    case 'config': {
      const settings = getAllSettings(vaultPath);
      console.log(JSON.stringify(settings, null, 2));
      break;
    }

    case 'init': {
      const folders = ensureBrainFolders(vaultPath);
      console.log(JSON.stringify(folders, null, 2));
      break;
    }

    case 'sync': {
      const result = options.dryRun ? analyzeSync() : runSync({ vaultPath });
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }

    case 'read': {
      const notePath = positional[1];
      if (!notePath) {
        console.error('Error: Note path required');
        process.exit(1);
      }
      const result = readNote(vaultPath, notePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }

    case 'create': {
      const notePath = positional[1];
      const content = positional[2] || '';
      if (!notePath) {
        console.error('Error: Note path required');
        process.exit(1);
      }
      const result = createNote(vaultPath, notePath, {
        content,
        frontmatter: options.frontmatter,
        overwrite: options.overwrite,
      });
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }

    case 'update': {
      const notePath = positional[1];
      const content = positional[2] || null;
      if (!notePath) {
        console.error('Error: Note path required');
        process.exit(1);
      }
      const result = updateNote(vaultPath, notePath, {
        content,
        frontmatter: options.frontmatter,
        mergeFrontmatter: options.merge,
      });
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }

    case 'delete': {
      const notePath = positional[1];
      if (!notePath) {
        console.error('Error: Note path required');
        process.exit(1);
      }
      const result = deleteNote(vaultPath, notePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }

    case 'list': {
      const folder = positional[1] || '';
      const result = listNotes(vaultPath, folder);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }

    case 'search': {
      const query = positional[1];
      if (!query) {
        console.error('Error: Search query required');
        process.exit(1);
      }

      let result;
      const searchOptions = { caseSensitive: options.caseSensitive };

      if (options.fuzzy) {
        result = searchNotesFuzzy(vaultPath, query, searchOptions);
        result.searchMode = 'fuzzy';
      } else if (options.regex) {
        result = searchNotesRegex(vaultPath, query, searchOptions);
        result.searchMode = 'regex';
      } else {
        result = searchNotes(vaultPath, query, searchOptions);
        result.searchMode = 'case-insensitive';
      }

      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'exists': {
      const notePath = positional[1];
      if (!notePath) {
        console.error('Error: Note path required');
        process.exit(1);
      }
      const exists = noteExists(vaultPath, notePath);
      console.log(JSON.stringify({ exists }, null, 2));
      process.exit(exists ? 0 : 1);
      break;
    }

    // ========================
    // CAPTURE COMMANDS
    // ========================
    case 'capture': {
      const captureType = positional[1];

      if (!captureType) {
        console.error('Error: Capture type required (thought, research, conversation)');
        process.exit(1);
      }

      switch (captureType) {
        case 'thought': {
          const thought = positional[2];
          if (!thought) {
            console.error('Error: Thought text required');
            process.exit(1);
          }

          const timestamp = getTimestamp();
          const dateStr = timestamp.split('T')[0];
          const noteId = generateNoteId();
          const notePath = `Brain/Thoughts/${dateStr}-${noteId}`;

          const result = createNote(vaultPath, notePath, {
            content: thought,
            frontmatter: {
              type: 'thought',
              created: timestamp,
              source: 'brain-cli',
            },
          });

          console.log(JSON.stringify({ ...result, captured: 'thought', noteId }, null, 2));
          process.exit(result.success ? 0 : 1);
          break;
        }

        case 'research': {
          if (!options.url) {
            console.error('Error: --url required for research capture');
            process.exit(1);
          }

          const timestamp = getTimestamp();
          const dateStr = timestamp.split('T')[0];
          const noteId = generateNoteId();
          const title = options.title || 'Research Note';
          const safeTitle = title.replace(/[^a-zA-Z0-9\s-]/g, '').replace(/\s+/g, '-').slice(0, 50);
          const notePath = `Brain/Research/${dateStr}-${safeTitle}-${noteId}`;

          const content = options.text || '';
          const fullContent = `[${title}](${options.url})\n\n${content}`;

          const result = createNote(vaultPath, notePath, {
            content: fullContent,
            frontmatter: {
              type: 'research',
              created: timestamp,
              url: options.url,
              title: options.title || 'Untitled',
              source: 'brain-cli',
            },
          });

          console.log(JSON.stringify({ ...result, captured: 'research', noteId }, null, 2));
          process.exit(result.success ? 0 : 1);
          break;
        }

        case 'conversation': {
          if (!options.source || !options.id) {
            console.error('Error: --source and --id required for conversation capture');
            process.exit(1);
          }

          const timestamp = getTimestamp();
          const dateStr = timestamp.split('T')[0];
          const noteId = generateNoteId();
          const notePath = `Brain/Conversations/${dateStr}-${options.source}-${noteId}`;

          const content = options.text || '';

          const result = createNote(vaultPath, notePath, {
            content: content,
            frontmatter: {
              type: 'conversation',
              created: timestamp,
              source: options.source,
              conversation_id: options.id,
              source: 'brain-cli',
            },
          });

          console.log(JSON.stringify({ ...result, captured: 'conversation', noteId }, null, 2));
          process.exit(result.success ? 0 : 1);
          break;
        }

        default:
          console.error(`Unknown capture type: ${captureType}`);
          showHelp();
          process.exit(1);
      }
      break;
    }

    // ========================
    // RESURFACE COMMANDS
    // ========================
    case 'resurface': {
      const resurfaceType = positional[1];

      if (!resurfaceType) {
        console.error('Error: Resurface type required (topic, stale)');
        process.exit(1);
      }

      switch (resurfaceType) {
        case 'topic': {
          const query = positional[2];
          if (!query) {
            console.error('Error: Search query required');
            process.exit(1);
          }

          // Use fuzzy search for topic resurfacing (better relevance)
          const result = searchNotesFuzzy(vaultPath, query, { threshold: 0.5 });

          if (!result.success) {
            console.log(JSON.stringify(result, null, 2));
            process.exit(1);
          }

          // Score based on fuzzy match quality (already ranked by score)
          const limited = result.results.slice(0, options.limit);
          const withRelevance = limited.map((item, index) => ({
            ...item,
            relevance: item.bestScore >= 0.9 ? 5 :
                       item.bestScore >= 0.8 ? 4 :
                       item.bestScore >= 0.7 ? 3 :
                       item.bestScore >= 0.6 ? 2 : 1,
            rank: index + 1,
          }));

          const output = {
            success: true,
            query,
            totalMatches: result.results.length,
            shown: withRelevance.length,
            searchMode: 'fuzzy',
            results: withRelevance,
          };

          console.log(JSON.stringify(output, null, 2));
          break;
        }

        case 'stale': {
          const days = options.days;
          const cutoffDate = new Date();
          cutoffDate.setDate(cutoffDate.getDate() - days);

          // Walk the vault to find all markdown files
          const findStale = (dir, relativePath = '') => {
            const staleFiles = [];
            const entries = fs.readdirSync(dir, { withFileTypes: true });

            for (const entry of entries) {
              const fullPath = path.join(dir, entry.name);
              const relPath = path.join(relativePath, entry.name);

              if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== '.obsidian') {
                staleFiles.push(...findStale(fullPath, relPath));
              } else if (entry.isFile() && entry.name.endsWith('.md')) {
                const stats = fs.statSync(fullPath);
                if (stats.mtime < cutoffDate) {
                  staleFiles.push({
                    path: relPath,
                    fullPath,
                    lastModified: stats.mtime.toISOString(),
                    daysUntouched: Math.floor((Date.now() - stats.mtime.getTime()) / (1000 * 60 * 60 * 24)),
                  });
                }
              }
            }

            return staleFiles;
          };

          const staleFiles = findStale(vaultPath);

          // Sort by oldest first
          staleFiles.sort((a, b) => new Date(a.lastModified) - new Date(b.lastModified));

          const output = {
            success: true,
            daysThreshold: days,
            totalStale: staleFiles.length,
            results: staleFiles.slice(0, options.limit),
          };

          console.log(JSON.stringify(output, null, 2));
          break;
        }

        default:
          console.error(`Unknown resurface type: ${resurfaceType}`);
          showHelp();
          process.exit(1);
      }
      break;
    }

    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }
}

main().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
