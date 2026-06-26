import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import type { Property } from './types'
import { LABELS } from './labels'
import { STATUS_OPTIONS, displayStatus } from './constants'
import { formatPriceFull } from './utils'

export type ColKey =
  | 'name' | 'price' | 'status' | 'address' | 'bedrooms' | 'bathrooms'
  | 'sqft' | 'year_built' | 'land_sqft' | 'parking_garage' | 'ac'
  | 'monthly_total' | 'hoa_monthly' | 'property_tax' | 'skytrain'

export type ColDef = { key: ColKey; label: string; render: (p: Property) => React.ReactNode }

export const ALL_COLUMNS: ColDef[] = [
  { key: 'name', label: 'Name', render: p => p.title },
  { key: 'price', label: 'Price', render: p => formatPriceFull(p.price, p.price_currency) ?? '—' },
  { key: 'status', label: 'Status', render: p => displayStatus(p.status) || '—' },
  { key: 'address', label: 'Address', render: p => [p.street_address, p.city].filter(Boolean).join(', ') || '—' },
  { key: 'bedrooms', label: 'Beds', render: p => p.bedrooms ?? '—' },
  { key: 'bathrooms', label: 'Baths', render: p => p.bathrooms ?? '—' },
  { key: 'sqft', label: LABELS.LIVING_AREA, render: p => p.sqft?.toLocaleString() ?? '—' },
  { key: 'year_built', label: LABELS.YEAR_BUILT, render: p => p.year_built ?? '—' },
  { key: 'land_sqft', label: LABELS.LOT_SIZE, render: p => p.land_sqft?.toLocaleString() ?? '—' },
  { key: 'parking_garage', label: LABELS.GARAGE, render: p => p.parking_garage ?? '—' },
  { key: 'ac', label: LABELS.AIR_CONDITIONING, render: p => p.ac === null ? '—' : p.ac ? 'Yes' : 'No' },
  { key: 'monthly_total', label: 'Monthly Total', render: p => p.monthly_total ? `$${p.monthly_total.toLocaleString()}` : '—' },
  { key: 'hoa_monthly', label: 'HOA', render: p => p.hoa_monthly ? `$${p.hoa_monthly.toLocaleString()}` : '—' },
  { key: 'property_tax', label: 'Tax/yr', render: p => p.property_tax ? `$${p.property_tax.toLocaleString()}` : '—' },
  { key: 'skytrain', label: 'Skytrain', render: p => p.skytrain_station ? `${p.skytrain_station} (${p.skytrain_walk_min ?? '?'} min)` : '—' },
]

export const DEFAULT_COLS: ColKey[] = ['name', 'price', 'monthly_total', 'status', 'bedrooms', 'bathrooms', 'sqft']

type SortKey = 'status' | 'monthly_total'
type SortDir = 'asc' | 'desc'

const STATUS_RANK = Object.fromEntries(STATUS_OPTIONS.map((s, i) => [s, i]))

function sortRows(rows: Property[], key: SortKey, dir: SortDir): Property[] {
  return [...rows].sort((a, b) => {
    let cmp = 0
    if (key === 'status') {
      const ra = STATUS_RANK[a.status] ?? 99
      const rb = STATUS_RANK[b.status] ?? 99
      cmp = ra - rb
    } else if (key === 'monthly_total') {
      const va = a.monthly_total ?? Infinity
      const vb = b.monthly_total ?? Infinity
      cmp = va - vb
    }
    return dir === 'asc' ? cmp : -cmp
  })
}

export function ListingTable({ rows, cols }: { rows: Property[]; cols: ColDef[] }) {
  const navigate = useNavigate()
  const [sortKey, setSortKey] = useState<SortKey>('status')
  const [sortDir, setSortDir] = useState<SortDir>('asc')

  function handleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  const sorted = sortRows(rows, sortKey, sortDir)
  const sortIcon = (key: SortKey) => sortKey === key ? (sortDir === 'asc' ? ' ▲' : ' ▼') : ' ⇅'

  return (
    <div className="table-wrap">
      <table className="listings-table">
        <thead>
          <tr>
            {cols.map(c => {
              const sortable = c.key === 'status' || c.key === 'monthly_total'
              return (
                <th
                  key={c.key}
                  onClick={sortable ? () => handleSort(c.key as SortKey) : undefined}
                  style={sortable ? { cursor: 'pointer', userSelect: 'none' } : undefined}
                >
                  {c.label}{sortable ? <span style={{ opacity: sortKey === c.key ? 1 : 0.35 }}>{sortIcon(c.key as SortKey)}</span> : null}
                </th>
              )
            })}
          </tr>
        </thead>
        <tbody>
          {sorted.map(p => (
            <tr key={p.id} onClick={() => navigate(`/property/${p.id}`)} className="table-row">
              {cols.map(c => <td key={c.key}>{c.render(p)}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

