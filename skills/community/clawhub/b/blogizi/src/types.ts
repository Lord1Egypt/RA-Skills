export interface Config {
  apiKey: string
  apiUrl: string // default: https://blogizi.com
  /** Active project slug for CLI draft/publish when using an account API key */
  projectSlug?: string
}

export interface PostFrontmatter {
  title: string
  description: string
  keyword: string
  slug: string
  status: 'draft' | 'published'
  date: string
  readingTime: number
  wordCount: number
}

export interface ParsedPost {
  frontmatter: PostFrontmatter
  content: string
  raw: string
}
