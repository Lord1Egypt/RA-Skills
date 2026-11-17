import matter from 'gray-matter'
import type { ParsedPost, PostFrontmatter } from '../types.js'

function normalize(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '')
}

// AI providers frequently restate the title as the first heading, even when
// told not to — the page already shows the title separately, so strip it
// here deterministically instead of relying on the prompt being followed.
function stripDuplicateTitleHeading(content: string, title: string): string {
  const trimmed = content.replace(/^\s+/, '')
  const match = trimmed.match(/^(#{1,6})[ \t]+(.+?)[ \t]*\n+/)
  if (!match) return content

  const [fullMatch, , headingText] = match
  if (normalize(headingText) !== normalize(title)) return content

  return trimmed.slice(fullMatch.length)
}

export function parsePost(raw: string): ParsedPost {
  const { data, content: rawContent } = matter(raw)

  const title = data.title || 'Untitled'
  const content = stripDuplicateTitleHeading(rawContent, title)

  const wordCount = content
    .replace(/```[\s\S]*?```/g, '')
    .replace(/[#*`_~\[\]]/g, '')
    .split(/\s+/)
    .filter(Boolean).length

  const readingTime = Math.ceil(wordCount / 200)

  const frontmatter: PostFrontmatter = {
    title,
    description: data.description || '',
    keyword: data.keyword || '',
    slug: data.slug || 'untitled',
    status: data.status || 'draft',
    date: data.date || new Date().toISOString().split('T')[0],
    readingTime,
    wordCount,
  }

  return { frontmatter, content, raw: matter.stringify(content, { ...frontmatter }) }
}
