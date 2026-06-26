import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import './App.css'
import { ListingGrid } from './ListingGrid'
import { ListingTable, ALL_COLUMNS, DEFAULT_COLS } from './ListingTable'
import type { ColKey } from './ListingTable'
import { STATUS_OPTIONS, STATUS_COLORS, HUMAN_PENDING_STATUS, USER_STATUSES, displayStatus } from './constants'
import type { StatusOption } from './constants'
import type { Property, SearchProfile } from './types'

function App() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [url, setUrl] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [listings, setListings] = useState<Property[]>([])
  const [statusFilter, setStatusFilter] = useState<Set<StatusOption>>(() => {
    const p = searchParams.get('status')
    if (p) {
      const parsed = p.split(',').filter(s => STATUS_OPTIONS.includes(s as StatusOption)) as StatusOption[]
      if (parsed.length > 0) return new Set(parsed)
    }
    const saved = localStorage.getItem('az_status_filter')
    if (saved) {
      const parsed = saved.split(',').filter(s => STATUS_OPTIONS.includes(s as StatusOption)) as StatusOption[]
      if (parsed.length > 0) return new Set(parsed)
    }
    return new Set<StatusOption>(['Interested', 'Buyable'])
  })
  const [viewMode, setViewMode] = useState<'grid' | 'table'>(() => {
    const saved = localStorage.getItem('az_view_mode')
    return saved === 'table' ? 'table' : 'grid'
  })
  const [visibleCols, setVisibleCols] = useState<Set<ColKey>>(new Set(DEFAULT_COLS))
  const [colPickerOpen, setColPickerOpen] = useState(false)

  // ── Search Profiles ───────────────────────────────────────────────────────
  const [searchProfiles, setSearchProfiles] = useState<SearchProfile[]>([])
  const [activeSearchId, setActiveSearchId] = useState<number | null>(() => {
    const p = searchParams.get('search')
    return p ? Number(p) : null
  })
  const [newSearchOpen, setNewSearchOpen] = useState(false)
  const [newSearchTitle, setNewSearchTitle] = useState('')
  const [newSearchDesc, setNewSearchDesc] = useState('')
  const [creatingSrch, setCreatingSrch] = useState(false)
  const [dragSrcId, setDragSrcId] = useState<number | null>(null)
  const [dragOverId, setDragOverId] = useState<number | null>(null)

  // ── Menu ──────────────────────────────────────────────────────────────────
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()

  // Sync filters back to URL so back-navigation restores them
  useEffect(() => {
    const params: Record<string, string> = {}
    if (statusFilter.size > 0) params.status = [...statusFilter].join(',')
    if (activeSearchId !== null) params.search = String(activeSearchId)
    setSearchParams(params, { replace: true })
  }, [statusFilter, activeSearchId])

  // Persist preferences across sessions
  useEffect(() => {
    localStorage.setItem('az_status_filter', [...statusFilter].join(','))
  }, [statusFilter])
  useEffect(() => {
    localStorage.setItem('az_view_mode', viewMode)
  }, [viewMode])

  async function fetchSearchProfiles() {
    try {
      const resp = await fetch('/api/search-profiles')
      if (resp.ok) {
        const data: SearchProfile[] = await resp.json()
        setSearchProfiles(data)
        // Auto-select first search if none selected or the selected one no longer exists
        if (data.length > 0) {
          const validId = activeSearchId !== null && data.some(s => s.id === activeSearchId)
          if (!validId) setActiveSearchId(data[0].id)
        }
      }
    } catch {
      // non-fatal
    }
  }

  async function fetchListings(searchProfileId: number) {
    const params = new URLSearchParams()
    params.set('search_profile_id', String(searchProfileId))
    const qs = params.toString() ? '?' + params.toString() : ''
    try {
      const resp = await fetch(`/api/listings${qs}`)
      if (resp.ok) setListings(await resp.json())
    } catch {
      // non-fatal
    }
  }

  useEffect(() => { fetchSearchProfiles() }, [])
  useEffect(() => { if (activeSearchId !== null) fetchListings(activeSearchId) }, [activeSearchId])

  async function handleCreateSearch(e: React.FormEvent) {
    e.preventDefault()
    if (!newSearchTitle.trim()) return
    setCreatingSrch(true)
    try {
      const resp = await fetch('/api/search-profiles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newSearchTitle.trim(), description: newSearchDesc.trim() }),
      })
      if (resp.ok) {
        const created: SearchProfile = await resp.json()
        setNewSearchTitle('')
        setNewSearchDesc('')
        setNewSearchOpen(false)
        await fetchSearchProfiles()
        setActiveSearchId(created.id)
      }
    } catch { /* non-fatal */ } finally {
      setCreatingSrch(false)
    }
  }

  function toggleStatus(s: StatusOption) {
    setStatusFilter(prev => {
      const next = new Set(prev)
      if (next.has(s)) { next.delete(s) } else { next.add(s) }
      return next
    })
  }

  const pendingListings = listings.filter(p => p.status === HUMAN_PENDING_STATUS)
  const reviewedListings = listings.filter(p => p.status !== HUMAN_PENDING_STATUS)

  const statusCounts = Object.fromEntries(
    STATUS_OPTIONS.map(s => [
      s,
      s === HUMAN_PENDING_STATUS
        ? pendingListings.length
        : reviewedListings.filter(p => p.status === s).length,
    ])
  ) as Record<StatusOption, number>

  const filteredListings = statusFilter.size > 0
    ? listings.filter(p => statusFilter.has(p.status as StatusOption))
    : reviewedListings

  const [savedInfo, setSavedInfo] = useState<{ id: number; title: string } | null>(null)
  const [dupInfo, setDupInfo] = useState<{ id: number; title: string; mls: string | null } | null>(null)

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSavedInfo(null)
    setDupInfo(null)
    if (!url.trim()) return setError('Please enter a URL')
    setSaving(true)
    try {
      const resp = await fetch('/api/listings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url.trim(), search_profile_id: activeSearchId }),
      })
      if (!resp.ok) {
        const text = await resp.text()
        if (resp.status === 409) {
          try {
            const body = JSON.parse(text)
            if (body.duplicate) {
              setDupInfo({ id: body.existing_id, title: body.existing_title, mls: body.mls_number })
              return
            }
          } catch { /* fall through to generic error */ }
        }
        throw new Error(text)
      }
      const saved: Property = await resp.json()
      setSavedInfo({ id: saved.id, title: saved.title || saved.redfin_url || saved.realtor_url || saved.zillow_url || `Listing #${saved.id}` })
      setUrl('')
      if (activeSearchId !== null) await fetchListings(activeSearchId)
      await fetchSearchProfiles()
    } catch (err: any) {
      setError(err?.message || String(err))
    } finally {
      setSaving(false)
    }
  }

  const activeSearch = searchProfiles.find(s => s.id === activeSearchId) ?? null

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="app-header-brand">
          <h1>Agent Zero</h1>
          <p className="app-tagline">AI-powered research — there's a perfect home for everybody</p>
        </div>
        {/* ── Header right ── */}
        <div className="app-header-right">
          <button className="inbox-link-btn" onClick={() => navigate('/inbox')}>
            {pendingListings.length > 0 && (
              <span className="inbox-link-badge">{pendingListings.length}</span>
            )}
            Inbox
          </button>
          <div className="app-menu-wrap">
            <button
              className="app-menu-btn"
              onClick={() => setMenuOpen(o => !o)}
              aria-label="Menu"
            >
              <span /><span /><span />
            </button>
            {menuOpen && (
              <>
                <div className="app-menu-backdrop" onClick={() => setMenuOpen(false)} />
                <ul className="app-menu-dropdown">
                  <li>
                    <button onClick={() => { setMenuOpen(false); navigate('/search-profiles') }}>
                      Manage Scenarios
                    </button>
                  </li>
                </ul>
              </>
            )}
          </div>
        </div>
      </header>

      {/* ── Search tabs (drag to reorder) ── */}
      <div className="search-tabs-wrap">
        <nav className="search-tabs">
          {searchProfiles.map(s => (
            <button
              key={s.id}
              className={`search-tab${s.id === activeSearchId ? ' active' : ''}${dragOverId === s.id ? ' drag-over' : ''}`}
              onClick={() => setActiveSearchId(s.id)}
              title={s.description || s.title}
              draggable
              onDragStart={e => { e.dataTransfer.effectAllowed = 'move'; setDragSrcId(s.id) }}
              onDragOver={e => { e.preventDefault(); setDragOverId(s.id) }}
              onDragLeave={() => setDragOverId(null)}
              onDrop={async e => {
                e.preventDefault()
                setDragOverId(null)
                if (dragSrcId === null || dragSrcId === s.id) return
                const ids = searchProfiles.map(x => x.id)
                const fromIdx = ids.indexOf(dragSrcId)
                const toIdx = ids.indexOf(s.id)
                if (fromIdx < 0 || toIdx < 0) return
                ids.splice(fromIdx, 1)
                ids.splice(toIdx, 0, dragSrcId)
                // Optimistic reorder
                const reordered = ids.map((id, i) => {
                  const orig = searchProfiles.find(x => x.id === id)!
                  return { ...orig, position: i }
                })
                setSearchProfiles(reordered)
                setDragSrcId(null)
                await fetch('/api/search-profiles/reorder', {
                  method: 'PUT',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ ids }),
                })
                await fetchSearchProfiles()
              }}
              onDragEnd={() => { setDragSrcId(null); setDragOverId(null) }}
            >
              {s.title}
              <span className="search-tab-count">{s.listing_count}</span>
            </button>
          ))}
        </nav>
        <button
          className={`search-tabs-add${newSearchOpen ? ' active' : ''}`}
          onClick={() => setNewSearchOpen(o => !o)}
          title="New scenario"
          aria-label="New scenario"
        >
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <path d="M6 1v10M1 6h10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          </svg>
        </button>
      </div>

      {newSearchOpen && (
        <form className="new-search-form" onSubmit={handleCreateSearch}>
          <input
            className="new-search-title"
            placeholder="Scenario title (e.g. East Van House)"
            value={newSearchTitle}
            onChange={e => setNewSearchTitle(e.target.value)}
            autoFocus
          />
          <textarea
            className="new-search-desc"
            placeholder="Describe what you're looking for… (optional)"
            value={newSearchDesc}
            onChange={e => setNewSearchDesc(e.target.value)}
            rows={3}
          />
          <div className="new-search-actions">
            <button type="submit" disabled={creatingSrch || !newSearchTitle.trim()}>
              {creatingSrch ? 'Creating…' : 'Create Scenario'}
            </button>
            <button type="button" className="cancel-btn" onClick={() => setNewSearchOpen(false)}>Cancel</button>
          </div>
        </form>
      )}

      {activeSearch && activeSearch.description && (
        <div className="search-desc">{activeSearch.description}</div>
      )}

      <form className="form-wrap">
        <div className="input-row">
          <input
            type="url"
            placeholder="Redfin, rew.ca, or Zillow URL"
            value={url}
            onChange={(e) => {
              const raw = e.target.value
              try {
                const u = new URL(raw)
                u.search = ''
                setUrl(u.toString())
              } catch {
                setUrl(raw)
              }
            }}
          />
          <button type="submit" onClick={handleSave} disabled={saving}>
            {saving ? 'Saving…' : 'Save'}
          </button>
        </div>
      </form>

      {error && <div className="message error">{error}</div>}
      {dupInfo && (
        <div className="message success">
          Already saved{dupInfo.mls ? ` (MLS ${dupInfo.mls})` : ''}: <a href={`/property/${dupInfo.id}`}>{dupInfo.title || `Listing #${dupInfo.id}`}</a>
        </div>
      )}
      {savedInfo && (
        <div className="message success">
          Saved: <a href={`/property/${savedInfo.id}`}>{savedInfo.title}</a>
        </div>
      )}

      <section className="listings-section">
        <div className="listings-header">
          <div className="status-filter">
            {USER_STATUSES.map((s) => (
              <button
                key={s}
                className={`filter-btn${statusFilter.has(s) ? ' active' : ''}`}
                onClick={() => toggleStatus(s)}
                style={statusFilter.has(s) ? { background: STATUS_COLORS[s], color: '#fff', borderColor: STATUS_COLORS[s] } : {}}
              >
                {displayStatus(s)} · {statusCounts[s]}
              </button>
            ))}
          </div>

          <div className="view-controls">
            <button className={`view-btn${viewMode === 'grid' ? ' active' : ''}`} onClick={() => setViewMode('grid')}>Grid</button>
            <button className={`view-btn${viewMode === 'table' ? ' active' : ''}`} onClick={() => setViewMode('table')}>Table</button>
            {viewMode === 'table' && (
              <div className="col-picker-wrap">
                <button className="view-btn" onClick={() => setColPickerOpen(o => !o)}>Columns ▾</button>
                {colPickerOpen && (
                  <div className="col-picker-dropdown">
                    {ALL_COLUMNS.map(c => (
                      <label key={c.key} className="col-picker-item">
                        <input
                          type="checkbox"
                          checked={visibleCols.has(c.key)}
                          onChange={() => setVisibleCols(prev => {
                            const next = new Set(prev)
                            if (next.has(c.key)) { next.delete(c.key) } else { next.add(c.key) }
                            return next
                          })}
                        />
                        {c.label}
                      </label>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {filteredListings.length > 0 ? (
          viewMode === 'grid' ? (
            <ListingGrid rows={[...filteredListings].sort((a, b) => {
              const ra = STATUS_OPTIONS.indexOf(a.status as any)
              const rb = STATUS_OPTIONS.indexOf(b.status as any)
              return (ra === -1 ? 99 : ra) - (rb === -1 ? 99 : rb)
            })} />
          ) : (
            <ListingTable rows={filteredListings} cols={ALL_COLUMNS.filter(c => visibleCols.has(c.key))} />
          )
        ) : (
          <p className="empty">
            {listings.length === 0
              ? 'No listings saved yet. Paste a property URL above and click Save.'
              : 'No listings match the selected filters.'}
          </p>
        )}
      </section>
    </div>
  )
}

export default App
