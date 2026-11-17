import { readFileSync } from 'fs'
import matter from 'gray-matter'
import chalk from 'chalk'
import ora from 'ora'
import { requireConfig } from '../lib/config.js'
import { parsePost } from '../lib/parser.js'
import { publishPost } from '../lib/api.js'

function hasExplicitStatus(raw: string): boolean {
  const { data } = matter(raw)
  return data.status === 'draft' || data.status === 'published'
}

export async function updateCommand(filePath: string) {
  const config = requireConfig()

  const raw = readFileSync(filePath, 'utf-8')
  const post = parsePost(raw)
  const explicitStatus = hasExplicitStatus(raw)

  const spinner = ora('Updating post...').start()
  const result = await publishPost(config, post, {
    upsert: true,
    // Keep the live/draft status on the server unless the file sets it.
    status: explicitStatus ? post.frontmatter.status : null,
  })

  if (!result.success) {
    spinner.fail(`Failed: ${result.error}`)
    process.exit(1)
  }

  if (result.created) {
    spinner.succeed(
      `No existing post with slug "${post.frontmatter.slug}" — created a new one`,
    )
    if (result.url) {
      console.log(chalk.dim(result.url))
    }
    return
  }

  spinner.succeed(`Updated post "${post.frontmatter.slug}"`)
  if (result.url) {
    console.log(chalk.dim(result.url))
  }
}
