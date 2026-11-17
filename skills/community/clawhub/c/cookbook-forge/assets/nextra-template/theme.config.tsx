import type { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span style={{ fontWeight: 700 }}>{{BOOK_TITLE}}</span>,
  project: { link: '{{GITHUB_REPO_URL}}' },
  docsRepositoryBase: '{{GITHUB_REPO_URL}}/tree/main',
  darkMode: true,
  i18n: [
    { locale: 'zh', name: '简体中文' },
    { locale: 'en', name: 'English' }
  ],
  search: { placeholder: '搜索文档…' },
  editLink: { content: '在 GitHub 上编辑此页 →' },
  feedback: { content: '问题或建议？' },
  footer: { content: '© {{YEAR}} {{BOOK_TITLE}} · 基于 Nextra 构建' },
  toc: { backToTop: true }
}

export default config
