import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { STATUS_COLORS, USER_STATUSES, displayStatus } from './constants'
import type { Property } from './types'
import { formatPriceCompact } from './utils'

interface ReviewQueueProps {
  listings: Property[]
  onReviewed: (id: number, status: string) => void
}

export function ReviewQueue({ listings, onReviewed }: ReviewQueueProps) {
  const navigate = useNavigate()
  const [dismissing, setDismissing] = useState<Set<number>>(new Set())

  if (listings.length === 0) return null

  async function assign(id: number, status: string) {
    setDismissing(prev => new Set(prev).add(id))
    setTimeout(() => onReviewed(id, status), 280)
    try {
      await fetch(`/api/listings/${id}/details`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      })
    } catch { /* non-fatal — optimistic update already applied */ }
  }

  return (
    <section className="review-queue">
      <div className="review-queue-header">
        <span className="review-queue-badge">{listings.length}</span>
        <span className="review-queue-title">Needs review</span>
      </div>
      <div className="review-queue-list">
        {listings.map(p => {
          const img = p.images[0]?.url
          const stats = [
            p.bedrooms != null ? `${p.bedrooms} bd` : null,
            p.bathrooms != null ? `${p.bathrooms} ba` : null,
            p.sqft != null ? `${p.sqft.toLocaleString()} sqft` : null,
          ].filter(Boolean).join(' · ')
          return (
            <div
              key={p.id}
              className={`review-row${dismissing.has(p.id) ? ' dismissing' : ''}`}
            >
              <div className="review-row-thumb" onClick={() => navigate(`/property/${p.id}`)}>
                {img
                  ? <img src={img} alt={p.title} />
                  : <div className="review-row-thumb-empty" />
                }
              </div>
              <div className="review-row-info" onClick={() => navigate(`/property/${p.id}`)}>
                <div className="review-row-price">{formatPriceCompact(p.price) ?? '—'}</div>
                {p.street_address && <div className="review-row-address">{p.street_address}</div>}
                {stats && <div className="review-row-stats">{stats}</div>}
              </div>
              <div className="review-row-actions">
                {USER_STATUSES.map(s => (
                  <button
                    key={s}
                    className="review-pill"
                    style={{ '--pill-color': STATUS_COLORS[s] } as React.CSSProperties}
                    onClick={() => assign(p.id, s)}
                    disabled={dismissing.has(p.id)}
                  >
                    {displayStatus(s)}
                  </button>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
