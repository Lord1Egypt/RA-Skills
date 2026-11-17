import { requireConfig, saveConfig } from '../lib/config.js'
import chalk from 'chalk'

export async function useCommand(projectSlug: string) {
  const config = requireConfig()
  const slug = projectSlug.trim().toLowerCase()

  if (!slug) {
    console.error(chalk.red('Project slug is required'))
    process.exit(1)
  }

  saveConfig({
    ...config,
    projectSlug: slug,
  })

  console.log(chalk.green(`✓ Active project set to ${slug}`))
  console.log(chalk.dim(`Config saved to ~/.blogizi/config.json`))
}
