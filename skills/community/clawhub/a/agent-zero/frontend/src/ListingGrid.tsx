import { useNavigate } from 'react-router-dom'
import { STATUS_COLORS, displayStatus } from './constants'
import type { Property } from './types'
import { formatPriceCompact } from './utils'

function formatNotePreview(notes: string): string {
  return notes
    .replace(/\p{Emoji_Presentation}|\p{Extended_Pictographic}/gu, '')
    .replace(/\n\s*-\s*/g, '; ')   // newline-bullet → semicolon
    .replace(/^\s*-\s*/, '')        // strip leading dash
    .replace(/\s+-\s+/g, '; ')     // inline dash-separator → semicolon
    .replace(/\s+/g, ' ')
    .trim()
}

function StatusBadge({ status }: { status: string | null }) {
  if (!status) return null
  return (
    <span className="status-badge" style={{ background: STATUS_COLORS[status] ?? '#888' }}>
      {displayStatus(status)}
    </span>
  )
}

function ListingCard({ p }: { p: Property }) {
  const navigate = useNavigate()
  const img = p.images[0]?.url
  const statusColor = STATUS_COLORS[p.status] ?? '#e0dfd8'
  const address = p.street_address

  return (
    <button
      className="listing-card"
      onClick={() => navigate(`/property/${p.id}`)}
      type="button"
    >
      <div className="listing-img-wrap">
        {img
          ? <img src={img} alt={p.title} className="listing-img" />
          : <div className="listing-img-placeholder" />
        }
      </div>
      <div className="listing-body" style={{ borderLeft: `4px solid ${statusColor}` }}>
        <div className="listing-price-row">
          <div className="listing-price">{formatPriceCompact(p.price) ?? '—'}</div>
          <StatusBadge status={p.status} />
        </div>
        {address && <div className="listing-address">
          <svg width="9" height="12" viewBox="0 0 9 12" fill="currentColor" aria-hidden="true" className="listing-address-icon">
            <path d="M4.5 0C2.015 0 0 2.015 0 4.5c0 3.375 4.5 7.5 4.5 7.5S9 7.875 9 4.5C9 2.015 6.985 0 4.5 0zm0 6.125A1.625 1.625 0 1 1 4.5 2.875a1.625 1.625 0 0 1 0 3.25z"/>
          </svg>
          {address}
        </div>}
        <div className="listing-stats">
          {p.bedrooms != null && <span>{p.bedrooms} bd</span>}
          {p.bathrooms != null && <span>{p.bathrooms} ba</span>}
          {p.sqft != null && <span>{p.sqft.toLocaleString()} sqft</span>}
          {p.year_built != null && <span>Built {p.year_built}</span>}
        </div>
        {p.notes && <div className="listing-notes">💬 {formatNotePreview(p.notes)}</div>}
      </div>
    </button>
  )
}

export function ListingGrid({ rows }: { rows: Property[] }) {
  return (
    <div className="listings-grid">
      {rows.map(p => <ListingCard key={p.id} p={p} />)}
    </div>
  )
}
