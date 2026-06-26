import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import type { Property, SearchProfile } from './types'
import { STATUS_COLORS, HUMAN_PENDING_STATUS, displayStatus } from './constants'
import { formatPriceCompact } from './utils'
import { PropertyDetailContent } from './PropertyDetail'
import './App.css'

// the inbox is a simple triage tool; the only statuses we offer here are
// 'Interested' or 'Pass'.  keeping the list in a constant makes it easier to
// modify later if requirements change.
const INBOX_ACTION_STATUSES = ['Interested', 'Pass'] as const
const INBOX_ACTION_ICONS: Record<typeof INBOX_ACTION_STATUSES[number], string> = {
  Interested: '✓',
  Pass: '✕',
}

export function InboxPage() {
  const navigate = useNavigate()
  const [searchProfiles, setSearchProfiles] = useState<SearchProfile[]>([])
  const [listings, setListings] = useState<Property[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [dismissing, setDismissing] = useState<Set<number>>(new Set())
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      setLoading(true)
      try {
        const searchResp = await fetch('/api/search-profiles')
        if (!searchResp.ok) return
        const allSearchProfiles: SearchProfile[] = await searchResp.json()
        setSearchProfiles(allSearchProfiles)

        const results = await Promise.all(
          allSearchProfiles.map(s =>
            fetch(`/api/listings?search_profile_id=${s.id}`)
              .then(r => r.ok ? r.json() : [])
              .catch(() => [])
          )
        )
        const pending = (results.flat() as Property[])
          .filter(p => p.status === HUMAN_PENDING_STATUS)
          .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        setListings(pending)
        if (pending.length > 0) setSelectedId(pending[0].id)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const assign = useCallback(async (id: number, status: string) => {
    const idx = listings.findIndex(p => p.id === id)
    const next =
      listings.find((p, i) => i > idx && !dismissing.has(p.id)) ??
      listings.find((p, i) => i < idx && !dismissing.has(p.id))
    setSelectedId(next?.id ?? null)

    setDismissing(prev => new Set(prev).add(id))
    setTimeout(() => {
      setListings(prev => prev.filter(p => p.id !== id))
      setDismissing(prev => { const s = new Set(prev); s.delete(id); return s })
    }, 300)

    try {
      await fetch(`/api/listings/${id}/details`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      })
    } catch { /* non-fatal */ }
  }, [listings, dismissing])

  const selected = listings.find(p => p.id === selectedId) ?? null
  const searchMap = Object.fromEntries(searchProfiles.map(s => [s.id, s.title]))

  return (
    <div className="inbox-page">
      <div className="inbox-sticky-header">
        <div className="inbox-nav">
          <button className="back-btn" onClick={() => navigate('/')}>
            <svg width="7" height="12" viewBox="0 0 7 12" fill="none" aria-hidden="true">
              <path d="M6 1L1 6l5 5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            Back
          </button>
          <div className="inbox-nav-title">
            Inbox
            {listings.length > 0 && <span className="inbox-nav-count">{listings.length}</span>}
          </div>
        </div>

        {!loading && listings.length > 0 && (
          <div className="inbox-list">
            {listings.map(p => {
              const img = p.images[0]?.url
              return (
                <div
                  key={p.id}
                  className={[
                    'inbox-item',
                    p.id === selectedId ? 'selected' : '',
                    dismissing.has(p.id) ? 'dismissing' : '',
                  ].filter(Boolean).join(' ')}
                  onClick={() => setSelectedId(p.id)}
                >
                  <div className="inbox-item-thumb">
                    {img
                      ? <img src={img} alt={p.title} />
                      : <div className="inbox-item-thumb-empty" />
                    }
                  </div>
                  <div className="inbox-item-info">
                    <div className="inbox-item-price">
                      {formatPriceCompact(p.price) ?? '—'}
                      {p.source_status && <span className="inbox-source-status">{p.source_status}</span>}
                    </div>
                    {p.street_address && <div className="inbox-item-address">{p.street_address}</div>}
                    {p.search_profile_id != null && searchMap[p.search_profile_id] && (
                      <div className="inbox-item-search">{searchMap[p.search_profile_id]}</div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {loading ? (
        <div className="loading">Loading…</div>
      ) : listings.length === 0 ? (
        <div className="inbox-empty">
          <div className="inbox-empty-icon">✓</div>
          <div className="inbox-empty-title">All caught up</div>
          <div className="inbox-empty-sub">No properties waiting for review</div>
        </div>
      ) : selected && (
        <PropertyDetailContent
          key={selected.id}
          initialProperty={selected}
          embedded
          onAfterDelete={() => {
            setListings(prev => prev.filter(p => p.id !== selected.id))
            setSelectedId(null)
          }}
        />
      )}

      {!loading && selected && (
        <div className="inbox-float-actions">
          {INBOX_ACTION_STATUSES.map(s => (
            <button
              key={s}
              className="inbox-action-btn"
              style={{ '--btn-color': STATUS_COLORS[s] } as React.CSSProperties}
              onClick={() => assign(selected.id, s)}
              disabled={dismissing.has(selected.id)}
            >
              {INBOX_ACTION_ICONS[s]} {displayStatus(s)}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
