import { readFileSync } from 'fs'
import chalk from 'chalk'
import ora from 'ora'
import { requireConfig } from '../lib/config.js'
import { parsePost } from '../lib/parser.js'
import { publishPost } from '../lib/api.js'

export async function publishCommand(filePath: string) {
  const config = requireConfig()

  const raw = readFileSync(filePath, 'utf-8')
  const post = parsePost(raw)

  // Force status to published
  post.frontmatter.status = 'published'

  const spinner = ora('Publishing...').start()
  const result = await publishPost(config, post)

  if (!result.success) {
    spinner.fail(`Failed: ${result.error}`)
    process.exit(1)
  }

  spinner.succeed(`Published at ${result.url}`)
}
