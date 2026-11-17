import { readFileSync } from 'fs'
import chalk from 'chalk'
import ora from 'ora'
import { requireConfig } from '../lib/config.js'
import { parsePost } from '../lib/parser.js'
import { publishPost } from '../lib/api.js'

export async function draftCommand(filePath: string) {
  const config = requireConfig()

  const raw = readFileSync(filePath, 'utf-8')
  const post = parsePost(raw)

  // Force status to draft — same payload as publish, different visibility.
  post.frontmatter.status = 'draft'

  const spinner = ora('Saving draft...').start()
  const result = await publishPost(config, post)

  if (!result.success) {
    spinner.fail(`Failed: ${result.error}`)
    process.exit(1)
  }

  spinner.succeed('Saved as draft')
  console.log(
    chalk.dim(
      `Edit it at https://blogizi.com/dashboard/projects/${result.projectId}`,
    ),
  )
}
