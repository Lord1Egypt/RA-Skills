import type { Config, ParsedPost, PostFrontmatter } from '../types.js'

export type PublishPostOptions = {
  /** Match Obsidian: update by slug when the post already exists. */
  upsert?: boolean
  /**
   * When set, overrides frontmatter status in the request body.
   * When `null`, omit status so the server keeps the existing post's status on update.
   */
  status?: PostFrontmatter['status'] | null
}

export type PublishPostResult = {
  success: boolean
  url?: string
  projectId?: string
  created?: boolean
  error?: string
}

export async function publishPost(
  config: Config,
  post: ParsedPost,
  options: PublishPostOptions = {},
): Promise<PublishPostResult> {
  const url = `${config.apiUrl}/api/posts`

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${config.apiKey}`,
  }

  if (config.projectSlug) {
    headers['X-Blogizi-Project'] = config.projectSlug
  }

  const status =
    options.status === null
      ? undefined
      : (options.status ?? post.frontmatter.status)

  const res = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      title: post.frontmatter.title,
      slug: post.frontmatter.slug,
      description: post.frontmatter.description,
      keyword: post.frontmatter.keyword,
      content: post.content,
      frontmatter: post.frontmatter,
      ...(status !== undefined ? { status } : {}),
      ...(options.upsert ? { upsert: true } : {}),
      ...(config.projectSlug ? { projectSlug: config.projectSlug } : {}),
    }),
  })

  const json = await res.json()

  if (!res.ok) {
    return { success: false, error: json.error || 'Unknown error' }
  }

  const slug = json.data?.slug
  const projectSlug = json.project?.slug
  const projectId = json.project?.id
  return {
    success: true,
    url: `https://${projectSlug}.app.blogizi.com/${slug}`,
    projectId,
    created: json.created === true,
  }
}
