import nextra from 'nextra'

const withNextra = nextra({
  theme: 'nextra-theme-docs',
  themeConfig: './theme.config.tsx',
  defaultShowCopyCode: true,
  latex: {
    renderer: 'katex',
    options: { strict: 'ignore', trust: true, displayMode: false }
  },
  search: { codeblocks: false },
  mdxOptions: {
    rehypePrettyCodeOptions: { theme: 'github-dark-dimmed' }
  }
})

export default withNextra({
  output: 'standalone',
  i18n: {
    locales: ['zh', 'en'],
    defaultLocale: 'zh'
  },
  reactStrictMode: true,
  images: { unoptimized: true }
})
