'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'

interface Article {
  id: string
  title: string
  source: string
  category: string
  link: string
  published_at: string
  summary: string
}

export default function Home() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedSource, setSelectedSource] = useState<string>('')
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [sources, setSources] = useState<string[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  async function fetchArticles(append = false) {
    try {
      let url = `${API_BASE}/api/articles?page=${page}&limit=20`
      if (selectedSource) url += `&source=${encodeURIComponent(selectedSource)}`
      if (selectedCategory) url += `&category=${encodeURIComponent(selectedCategory)}`
      
      const res = await fetch(url)
      const data = await res.json()
      if (append) {
        setArticles(prev => [...prev, ...data])
      } else {
        setArticles(data)
      }
      setHasMore(data.length === 20)
    } catch (error) {
      console.error('Failed to fetch articles:', error)
    } finally {
      setLoading(false)
    }
  }

  async function fetchFilters() {
    try {
      const [sourcesRes, categoriesRes] = await Promise.all([
        fetch(`${API_BASE}/api/sources`),
        fetch(`${API_BASE}/api/categories`)
      ])
      setSources(await sourcesRes.json())
      setCategories(await categoriesRes.json())
    } catch (error) {
      console.error('Failed to fetch filters:', error)
    }
  }

  useEffect(() => {
    setPage(1)
    setArticles([])
    fetchArticles(false)
  }, [selectedSource, selectedCategory])

  useEffect(() => {
    fetchFilters()
  }, [])

  useEffect(() => {
    if (page > 1) {
      fetchArticles(true)
    }
  }, [page])

  function formatDate(dateStr: string) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  function loadMore() {
    setPage(p => p + 1)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-slate-700">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center font-bold text-xl">
                AI
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  AI资讯
                </h1>
                <p className="text-xs text-slate-400">实时聚合全球AI新闻</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => fetchArticles(false)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors"
              >
                刷新
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-wrap gap-3 mb-8">
          <select
            value={selectedSource}
            onChange={(e) => setSelectedSource(e.target.value)}
            className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">所有来源</option>
            {sources.map(s => <option key={s} value={s}>{s}</option>)}
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">所有分类</option>
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        {loading && articles.length === 0 && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <span className="ml-3 text-slate-400">加载中...</span>
          </div>
        )}

        {!loading && articles.length === 0 && (
          <div className="text-center py-20 text-slate-400">
            <p className="text-lg">暂无文章</p>
            <button
              onClick={() => fetchArticles(false)}
              className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors"
            >
              刷新重试
            </button>
          </div>
        )}

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {articles.map(article => (
            <a
              key={article.id}
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              className="group bg-slate-800/50 hover:bg-slate-800 border border-slate-700 hover:border-slate-600 rounded-2xl p-5 transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/10"
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="px-2 py-1 bg-blue-600/20 text-blue-400 text-xs font-medium rounded-full">
                  {article.source}
                </span>
                <span className="px-2 py-1 bg-purple-600/20 text-purple-400 text-xs font-medium rounded-full">
                  {article.category}
                </span>
              </div>
              
              <h3 className="font-semibold text-lg leading-tight mb-2 group-hover:text-blue-400 transition-colors line-clamp-3">
                {article.title}
              </h3>
              
              <p className="text-slate-400 text-sm line-clamp-3 mb-4">
                {article.summary.replace(/<[^>]*>/g, '')}
              </p>
              
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>{formatDate(article.published_at)}</span>
                <span className="group-hover:translate-x-1 transition-transform">
                  阅读全文 →
                </span>
              </div>
            </a>
          ))}
        </div>

        {hasMore && (
          <div className="text-center mt-12">
            <button
              onClick={loadMore}
              className="px-8 py-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl font-medium transition-colors"
            >
              加载更多
            </button>
          </div>
        )}
      </main>

      <footer className="border-t border-slate-800 mt-20">
        <div className="max-w-6xl mx-auto px-4 py-8 text-center text-slate-500 text-sm">
          <p>Powered by AI News Website Generator</p>
          <p className="mt-2">自动每6小时刷新 · 数据源: 全球科技媒体RSS</p>
        </div>
      </footer>
    </div>
  )
}
