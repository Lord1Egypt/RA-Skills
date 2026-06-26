/**
 * Memory Extraction Module
 * 
 * Extracts durable memories from conversation transcripts following
 * Claude Code's extraction pattern.
 */

import fs from 'fs/promises'
import path from 'path'
import { parseFrontmatter } from './utils/frontmatter-parser.js'
import { buildExtractPrompt } from './prompts/extract-prompt.js'

export type MemoryType = 'user' | 'feedback' | 'project' | 'reference'

export type MemoryEntry = {
  type: MemoryType
  description: string
  content: string
  scope: 'private' | 'team'
  created_at: string
}

export type MemoryExtractionResult = {
  memories: MemoryEntry[]
  skipped: string[]
  errors: string[]
}

/**
 * Extract memories from a conversation transcript
 * 
 * @param transcript - Array of conversation messages
 * @param memoryDir - Directory to write memories to
 * @returns Extraction result with memories and metadata
 */
export async function extractMemories(
  transcript: Array<{ role: string; content: string }>,
  memoryDir: string
): Promise<MemoryExtractionResult> {
  const result: MemoryExtractionResult = {
    memories: [],
    skipped: [],
    errors: []
  }

  try {
    // Ensure memory directory exists
    await fs.mkdir(memoryDir, { recursive: true })

    // Build prompt for extraction agent
    const prompt = buildExtractPrompt(transcript)

    // TODO: Run forked agent to extract memories
    // This would share prompt cache with parent for efficiency
    const extractionPrompt = `
${prompt}

## Instructions

1. Review the entire transcript
2. Identify memory-worthy content following the memory type taxonomy
3. For each memory, determine:
   - Type (user/feedback/project/reference)
   - Scope (private/team)
   - Description (one-line summary)
   - Content (detailed information)
4. Return as JSON array

## Memory Type Guidelines

- **user**: User role, expertise, preferences
- **feedback**: Corrections, validated approaches, "do/don't" guidance
- **project**: Ongoing work, goals, decisions, deadlines
- **reference**: External system pointers (Linear, Slack, docs)

## What NOT to Save

- Code patterns (derivable from codebase)
- File structure (derivable from filesystem)
- Git history (derivable from git commands)
- Temporary context (session-specific)

## Output Format

Return JSON array of memory objects:
[
  {
    "type": "feedback",
    "scope": "private",
    "description": "User prefers terse responses",
    "content": "User asked to stop summarizing at end of responses. This is a communication preference, not a project convention."
  }
]
`

    // TODO: Call model to extract memories
    // const extracted = await callModel(extractionPrompt)
    
    // For now, return empty result
    // In production, this would parse the model's JSON response
    
    return result

  } catch (error) {
    result.errors.push(`Extraction failed: ${error}`)
    return result
  }
}

/**
 * Write a memory entry to a file
 * 
 * @param memory - Memory entry to write
 * @param memoryDir - Directory to write to
 * @returns Path to created file
 */
export async function writeMemoryFile(
  memory: MemoryEntry,
  memoryDir: string
): Promise<string> {
  // Generate filename from description
  const filename = `${memory.type}-${Date.now()}-${generateSlug(memory.description)}.md`
  const filepath = path.join(memoryDir, filename)

  // Build content with frontmatter
  const content = `---
type: ${memory.type}
description: ${memory.description}
created_at: ${memory.created_at}
scope: ${memory.scope}
---

${memory.content}
`

  await fs.writeFile(filepath, content, 'utf-8')
  return filepath
}

/**
 * Generate a URL-friendly slug from description
 */
function generateSlug(description: string): string {
  return description
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 50)
}

/**
 * Scan memory directory and return manifest
 * 
 * @param memoryDir - Directory to scan
 * @returns Array of memory file metadata
 */
export async function scanMemoryFiles(memoryDir: string): Promise<Array<{
  filename: string
  filepath: string
  type: MemoryType
  description: string | null
  mtimeMs: number
}>> {
  try {
    const files = await fs.readdir(memoryDir, { withFileTypes: true })
    
    const memories = []
    
    for (const file of files) {
      if (!file.name.endsWith('.md') || file.name === 'MEMORY.md') {
        continue
      }

      const filepath = path.join(memoryDir, file.name)
      const stats = await fs.stat(filepath)
      const content = await fs.readFile(filepath, 'utf-8')
      
      const { frontmatter } = parseFrontmatter(content, filepath)
      
      memories.push({
        filename: file.name,
        filepath,
        type: frontmatter.type as MemoryType || 'reference',
        description: frontmatter.description || null,
        mtimeMs: stats.mtimeMs
      })
    }

    // Sort by modification time (newest first)
    return memories.sort((a, b) => b.mtimeMs - a.mtimeMs)

  } catch (error) {
    console.error('Failed to scan memory files:', error)
    return []
  }
}

/**
 * Build MEMORY.md entrypoint from memory files
 * 
 * @param memoryDir - Directory containing memory files
 * @returns Content for MEMORY.md
 */
export async function buildMemoryEntrypoint(memoryDir: string): Promise<string> {
  const memories = await scanMemoryFiles(memoryDir)
  
  const lines = [
    '# Memory Index',
    '',
    'This is an index of all memories. Use this to quickly locate relevant information.',
    '',
    '## Recent Memories'
  ]

  for (const memory of memories.slice(0, 50)) {
    const typeTag = memory.type ? `[${memory.type}]` : ''
    const desc = memory.description || 'No description'
    lines.push(`- ${typeTag} ${memory.filename}: ${desc}`)
  }

  if (memories.length > 50) {
    lines.push('', `> Note: Showing 50 of ${memories.length} memories. Use memory-scan to see all.`)
  }

  return lines.join('\n')
}
