import { LABELS } from './labels'

import { useEffect, useRef, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { marked } from 'marked'
import { emojify, get as getEmoji, search as searchEmoji } from 'node-emoji'
import type { Property, SearchProfile } from './types'
import { STATUS_COLORS, USER_STATUSES, displayStatus } from './constants'
import type { StatusOption } from './constants'
import { formatPriceFull } from './utils'

type PreviewResult =
    | { kind: 'status_only'; source_status: string }
    | { kind: 'full'; property: Property }

type HistoryEntry = {
    id: number
    listing_id: number
    field_name: string
    old_value: string | null
    new_value: string | null
    changed_at: string
}

// ── History field label map ───────────────────────────────────────────────────

const HISTORY_FIELD_LABELS: Record<string, string> = {
    price: 'Price',
    mls_number: 'MLS #',
    listed_date: 'Listed Date',
    source_status: 'Source Status',
}

function historyFieldLabel(name: string): string {
    return HISTORY_FIELD_LABELS[name] ?? name
}

function formatHistoryValue(field: string, value: string | null): string {
    if (value === null) return '—'
    if (field === 'price') {
        // Some history values may already be formatted, some may be raw numbers.
        const rawDigits = value.replace(/[^0-9\-]/g, '')
        const parsed = Number(rawDigits)
        if (!Number.isNaN(parsed)) {
            return formatPriceFull(parsed, 'CAD') ?? value
        }
    }
    return value
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function boolLabel(v: boolean | null): string {
    return v === null ? '—' : v ? 'Yes' : 'No'
}

function moneyLabel(v: number | null): string {
    return v === null ? '—' : `$${v.toLocaleString()}`
}

function numLabel(v: number | null, suffix = ''): string {
    return v === null ? '—' : `${v}${suffix}`
}

function formatImgDate(dateStr: string) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString('en-CA', {
        month: 'short', day: 'numeric', year: 'numeric',
    })
}

/** Compute standard monthly mortgage payment. */
function calcMortgage(price: number | null, downPct: number, rate: number, years: number): number | null {
    if (!price) return null
    const loan = price * (1 - downPct)
    if (loan <= 0) return 0
    const n = years * 12
    if (rate === 0) return Math.round(loan / n)
    const r = rate / 12
    return Math.round(loan * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1))
}

function calcMonthlyTotal(mortgageMonthly: number | null, propertyTaxAnnual: number | null, hoaMonthly: number | null): number | null {
    if (mortgageMonthly == null && propertyTaxAnnual == null && hoaMonthly == null) return null
    const taxMonthly = propertyTaxAnnual != null ? Math.floor(propertyTaxAnnual / 12) : 0
    return (mortgageMonthly ?? 0) + taxMonthly + (hoaMonthly ?? 0)
}

function calcInitialMonthlyInterest(price: number | null, downPct: number, annualRate: number): number | null {
    if (!price) return null
    const loan = price * (1 - downPct)
    if (loan <= 0) return 0
    return Math.round((loan * annualRate) / 12)
}

function moneyPart(v: number | null): string {
    return `$${(v ?? 0).toLocaleString()}`
}

type EmojiSuggestion = {
    name: string
    emoji: string
}

const EMOJI_ALIAS_TO_CANONICAL: Record<string, string> = {
    warn: 'warning',
    ok: 'white_check_mark',
    check: 'white_check_mark',
    xmark: 'x',
    nope: 'x',
}

const POPULAR_EMOJI_NAMES = [
    'warning',
    'white_check_mark',
    'x',
    'fire',
    'rocket',
    'hourglass',
    'eyes',
    'bulb',
    'star',
    'moneybag',
    'house',
    'key',
]

const POPULAR_EMOJI_SUGGESTIONS: EmojiSuggestion[] = POPULAR_EMOJI_NAMES
    .map(name => ({ name, emoji: getEmoji(name) }))
    .filter((item): item is EmojiSuggestion => typeof item.emoji === 'string')

function normalizeEmojiAliases(input: string): string {
    return input.replace(/:([a-z0-9_+-]+):/gi, (match, shortcode: string) => {
        const canonical = EMOJI_ALIAS_TO_CANONICAL[shortcode.toLowerCase()]
        return canonical ? `:${canonical}:` : match
    })
}

function replaceEmojiShortcodes(input: string): string {
    return emojify(normalizeEmojiAliases(input))
}

function detectEmojiQuery(input: string, caretPos: number): { start: number; end: number; query: string } | null {
    if (caretPos < 0 || caretPos > input.length) return null

    const beforeCaret = input.slice(0, caretPos)
    const start = beforeCaret.lastIndexOf(':')
    if (start < 0) return null

    if (start > 0) {
        const prevChar = input[start - 1]
        if (!/[\s([{"']/.test(prevChar)) return null
    }

    const query = input.slice(start + 1, caretPos)
    if (!/^[a-z0-9_+-]*$/i.test(query)) return null
    if (query.includes(':')) return null

    return { start, end: caretPos, query: query.toLowerCase() }
}

function buildEmojiSuggestions(query: string): EmojiSuggestion[] {
    if (!query) return POPULAR_EMOJI_SUGGESTIONS

    const canonical = EMOJI_ALIAS_TO_CANONICAL[query]
    const aliasSuggestion = canonical
        ? getEmoji(canonical)
            ? [{ name: query, emoji: getEmoji(canonical)! }]
            : []
        : []

    const results = searchEmoji(query)
        .slice(0, 20)
        .map(r => ({ name: r.name, emoji: r.emoji }))

    const deduped = new Map<string, EmojiSuggestion>()
    for (const item of [...aliasSuggestion, ...results]) {
        const key = `${item.name}:${item.emoji}`
        if (!deduped.has(key)) deduped.set(key, item)
        if (deduped.size >= 8) break
    }
    return Array.from(deduped.values())
}


// ── Edit helpers ──────────────────────────────────────────────────────────────

function NumInput({ label, value, onChange, suffix }: {
    label: string; value: number | null; onChange: (v: number | null) => void; suffix?: string
}) {
    return (
        <div className="tracked-field">
            <label>{label}{suffix ? ` (${suffix})` : ''}</label>
            <input
                className="edit-input"
                type="number"
                value={value ?? ''}
                onChange={e => onChange(e.target.value ? Number(e.target.value) : null)}
            />
        </div>
    )
}

function BoolSelect({ label, value, onChange }: {
    label: string; value: boolean | null; onChange: (v: boolean | null) => void
}) {
    return (
        <div className="tracked-field">
            <label>{label}</label>
            <select
                className="edit-input"
                value={value === null ? '' : value ? 'true' : 'false'}
                onChange={e => onChange(e.target.value === '' ? null : e.target.value === 'true')}
            >
                <option value="">—</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
            </select>
        </div>
    )
}

// ── Diff modal ────────────────────────────────────────────────────────────────

type DiffEntry = { field: string; old: string; fresh: string }

function RefreshDiffModal({
    diffs,
    onApply,
    onCancel,
    applying,
}: {
    diffs: DiffEntry[]
    onApply: () => void
    onCancel: () => void
    applying: boolean
}) {
    return (
        <div className="modal-overlay">
            <div className="modal">
                <h3>Changes found from source</h3>
                {diffs.length === 0 ? (
                    <p className="no-changes">No changes detected — listing is up to date.</p>
                ) : (
                    <table className="diff-table">
                        <thead>
                            <tr><th>Field</th><th>Stored</th><th>Fresh</th></tr>
                        </thead>
                        <tbody>
                            {diffs.map(d => (
                                <tr key={d.field}>
                                    <td className="diff-field">{d.field}</td>
                                    <td className="diff-old">{d.old}</td>
                                    <td className="diff-new">{d.fresh}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
                <div className="modal-actions">
                    {diffs.length > 0 && (
                        <button className="save-btn" onClick={onApply} disabled={applying}>
                            {applying ? 'Applying…' : 'Apply changes'}
                        </button>
                    )}
                    <button className="cancel-btn" onClick={onCancel} disabled={applying}>
                        {diffs.length === 0 ? 'Close' : 'Cancel'}
                    </button>
                </div>
            </div>
        </div>
    )
}

// ── Compare helper ────────────────────────────────────────────────────────────

function str(v: unknown): string {
    if (v === null || v === undefined) return '—'
    if (typeof v === 'boolean') return v ? 'Yes' : 'No'
    return String(v)
}

const TITLE_KEY: keyof Property = 'title'

const DIFF_FIELDS: { key: keyof Property; label: string }[] = [
    { key: TITLE_KEY, label: LABELS.TITLE },
    { key: 'price', label: LABELS.PRICE },
    { key: 'street_address', label: LABELS.ADDRESS },
    { key: 'city', label: LABELS.CITY },
    { key: 'region', label: LABELS.REGION },
    { key: 'postal_code', label: LABELS.POSTAL_CODE },
    { key: 'bedrooms', label: LABELS.BEDROOMS },
    { key: 'bathrooms', label: LABELS.BATHROOMS },
    { key: 'sqft', label: LABELS.LIVING_AREA },
    { key: 'year_built', label: LABELS.YEAR_BUILT },
    { key: 'land_sqft', label: LABELS.LOT_SIZE },
    { key: 'parking_garage', label: LABELS.GARAGE },
    { key: 'ac', label: LABELS.AIR_CONDITIONING },
    { key: 'radiant_floor_heating', label: LABELS.RADIANT_FLOOR_HEATING },
    { key: 'property_tax', label: LABELS.PROPERTY_TAX },
    { key: 'hoa_monthly', label: LABELS.HOA_MONTHLY },
    { key: 'school_elementary', label: LABELS.SCHOOL_ELEMENTARY },
    { key: 'school_middle', label: LABELS.SCHOOL_MIDDLE },
    { key: 'school_secondary', label: LABELS.SCHOOL_SECONDARY },
]

/** Mirror of `is_title_exist` in backend/src/api/refresh.rs — keep in sync. */
function isTitleExist(title: string): boolean {
    return title.length > 0
}

function fmtOpenHouse(oh: { start_time: string; end_time?: string | null }): string {
    const start = new Date(oh.start_time)
    const datePart = start.toLocaleDateString('en-CA', { weekday: 'short', month: 'short', day: 'numeric' })
    const startTime = start.toLocaleTimeString('en-CA', { hour: 'numeric', minute: '2-digit' })
    if (oh.end_time) {
        const endTime = new Date(oh.end_time).toLocaleTimeString('en-CA', { hour: 'numeric', minute: '2-digit' })
        return `${datePart} ${startTime}–${endTime}`
    }
    return `${datePart} ${startTime}`
}

function fmtOpenHouseList(openHouses: Property['open_houses']): string {
    if (openHouses.length === 0) return '—'
    return openHouses.map(fmtOpenHouse).join(', ')
}

function buildDiff(stored: Property, fresh: Property): DiffEntry[] {
    const diffs = DIFF_FIELDS
        .filter(f => str(stored[f.key]) !== str(fresh[f.key]))
        .filter(f => f.key !== TITLE_KEY || !isTitleExist(stored.title))
        .map(f => ({ field: f.label, old: str(stored[f.key]), fresh: str(fresh[f.key]) }))

    // Compare open houses by start_time set
    const storedTimes = new Set(stored.open_houses.map(oh => oh.start_time))
    const freshTimes = new Set(fresh.open_houses.map(oh => oh.start_time))
    const hasNew = fresh.open_houses.some(oh => !storedTimes.has(oh.start_time))
    const hasRemoved = stored.open_houses.some(oh => !freshTimes.has(oh.start_time))
    if (hasNew || hasRemoved) {
        diffs.push({ field: 'Open Houses', old: fmtOpenHouseList(stored.open_houses), fresh: fmtOpenHouseList(fresh.open_houses) })
    }

    return diffs
}

// ── Build details payload (all editable fields) ───────────────────────────────

function toUserDetails(p: Property) {
    return {
        title: p.title,
        price: p.price,
        price_currency: p.price_currency,
        offer_price: p.offer_price,
        street_address: p.street_address,
        city: p.city,
        region: p.region,
        postal_code: p.postal_code,
        bedrooms: p.bedrooms,
        bathrooms: p.bathrooms,
        sqft: p.sqft,
        year_built: p.year_built,
        parking_total: p.parking_total,
        parking_garage: p.parking_garage,
        parking_carport: p.parking_carport,
        parking_pad: p.parking_pad,
        land_sqft: p.land_sqft,
        property_tax: p.property_tax,
        skytrain_station: p.skytrain_station,
        skytrain_walk_min: p.skytrain_walk_min,
        radiant_floor_heating: p.radiant_floor_heating,
        ac: p.ac,
        down_payment_pct: p.down_payment_pct,
        mortgage_interest_rate: p.mortgage_interest_rate,
        amortization_years: p.amortization_years,
        hoa_monthly: p.hoa_monthly,
        monthly_total: p.monthly_total,
        monthly_cost: p.monthly_cost,
        has_rental_suite: p.has_rental_suite,
        rental_income: p.rental_income,
        status: p.status,
        school_elementary: p.school_elementary,
        school_elementary_rating: p.school_elementary_rating,
        school_middle: p.school_middle,
        school_middle_rating: p.school_middle_rating,
        school_secondary: p.school_secondary,
        school_secondary_rating: p.school_secondary_rating,
    }
}

// ── Main component ────────────────────────────────────────────────────────────

export function PropertyDetailContent({
    initialProperty,
    onAfterDelete,
    embedded = false,
}: {
    initialProperty: Property
    onAfterDelete?: () => void
    embedded?: boolean
}) {
    const [property, setProperty] = useState<Property>(initialProperty)
    const [error, setError] = useState<string | null>(null)
    const [refreshMsg, setRefreshMsg] = useState<string | null>(null)

    // Notes
    const [notes, setNotes] = useState<string>(initialProperty.notes ?? '')
    const [notesSaving, setNotesSaving] = useState(false)
    const [notesEditing, setNotesEditing] = useState(false)
    const notesInputRef = useRef<HTMLTextAreaElement>(null)
    const [emojiSuggestions, setEmojiSuggestions] = useState<EmojiSuggestion[]>([])
    const [emojiSuggestActiveIdx, setEmojiSuggestActiveIdx] = useState(0)
    const [emojiSuggestRange, setEmojiSuggestRange] = useState<{ start: number; end: number } | null>(null)

    // Title (inline header)
    const [titleDraft, setTitleDraft] = useState<string>(initialProperty.title ?? '')
    const [titleToast, setTitleToast] = useState(false)

    // Edit mode
    const [editMode, setEditMode] = useState(false)
    const [draft, setDraft] = useState<Property | null>(null)
    const [saving, setSaving] = useState(false)
    const [financeEditMode, setFinanceEditMode] = useState(false)
    const [financeSaving, setFinanceSaving] = useState(false)
    const [financeDraft, setFinanceDraft] = useState<Property | null>(null)
    const [locationEditMode, setLocationEditMode] = useState(false)
    const [locationSaving, setLocationSaving] = useState(false)
    const [locationDraft, setLocationDraft] = useState<{ skytrain_station: string | null; skytrain_walk_min: number | null } | null>(null)

    // Refresh preview
    const [previewing, setPreviewing] = useState(false)
    const [applying, setApplying] = useState(false)
    const [diffModal, setDiffModal] = useState<DiffEntry[] | null>(null)

    // Delete
    const [deleting, setDeleting] = useState(false)

    // Agent re-review
    const [agentReviewing, setAgentReviewing] = useState(false)
    const [agentReviewError, setAgentReviewError] = useState<string | null>(null)

    // URL draft (right panel — always editable, independent of main edit mode)
    const [urlDraft, setUrlDraft] = useState<{
        redfin_url: string | null
        realtor_url: string | null
        rew_url: string | null
        zillow_url: string | null
    }>({ redfin_url: initialProperty.redfin_url, realtor_url: initialProperty.realtor_url, rew_url: initialProperty.rew_url, zillow_url: initialProperty.zillow_url })
    const [editingUrlKey, setEditingUrlKey] = useState<'redfin_url' | 'realtor_url' | 'rew_url' | 'zillow_url' | null>(null)
    const [urlsSaving, setUrlsSaving] = useState(false)
    const [urlSaveError, setUrlSaveError] = useState<string | null>(null)
    const [urlsExpanded, setUrlsExpanded] = useState(false)

    // History expand
    const [historyExpanded, setHistoryExpanded] = useState(false)

    // Lightbox
    const [lightboxOpen, setLightboxOpen] = useState(false)
    const [activeIdx, setActiveIdx] = useState(0)
    const thumbsRef = useRef<HTMLDivElement>(null)
    const scrollRef = useRef<HTMLDivElement>(null)
    // Suppresses the onScroll sync while a programmatic scrollIntoView is animating
    const programmaticScroll = useRef(false)

    function goTo(next: number) {
        const clamped = Math.max(0, Math.min(next, property.images.length - 1))
        if (clamped === activeIdx) return
        programmaticScroll.current = true
        setActiveIdx(clamped)
        scrollRef.current?.querySelectorAll<HTMLElement>('.lightbox-item')[clamped]
            ?.scrollIntoView({ behavior: 'smooth', block: 'center' })
        thumbsRef.current?.querySelectorAll<HTMLElement>('.lightbox-thumb')[clamped]
            ?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
        setTimeout(() => { programmaticScroll.current = false }, 600)
    }

    useEffect(() => {
        if (!lightboxOpen) return
        function handleKey(e: KeyboardEvent) {
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault()
                goTo(e.key === 'ArrowDown' ? activeIdx + 1 : activeIdx - 1)
            } else if (e.key === 'Escape') {
                setLightboxOpen(false)
            }
        }
        window.addEventListener('keydown', handleKey)
        return () => window.removeEventListener('keydown', handleKey)
    }, [lightboxOpen, activeIdx, property.images.length])

    // History
    const [history, setHistory] = useState<HistoryEntry[]>([])

    useEffect(() => {
        fetch(`/api/listings/${initialProperty.id}/history`)
            .then(r => r.ok ? r.json() : [])
            .then(setHistory)
            .catch(() => {})
    }, [initialProperty.id])

    // ── Search profiles (for move-to-search-profile) ─────────────────────────
    const [searchProfiles, setSearchProfiles] = useState<SearchProfile[]>([])
    useEffect(() => {
        fetch('/api/search-profiles').then(r => r.ok ? r.json() : []).then(setSearchProfiles).catch(() => { })
    }, [])

    async function handleMoveToSearchProfile(searchProfileId: number) {
        try {
            const resp = await fetch(`/api/listings/${property.id}/search-profile`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ search_profile_id: searchProfileId }),
            })
            if (resp.ok) {
                setProperty(prev => ({ ...prev, search_profile_id: searchProfileId }))
                // refresh search profile counts
                fetch('/api/search-profiles').then(r => r.ok ? r.json() : []).then(setSearchProfiles).catch(() => { })
            }
        } catch { /* non-fatal */ }
    }

    // ── Edit mode ─────────────────────────────────────────────────────────────

    function enterEdit() {
        setDraft({ ...property })
        setEditMode(true)
    }

    function cancelEdit() {
        setEditMode(false)
        setDraft(null)
        setFinanceEditMode(false)
        setFinanceDraft(null)
    }

    function setDraftField<K extends keyof Property>(key: K, val: Property[K]) {
        setDraft(d => d ? { ...d, [key]: val } : d)
    }

    /** Recalculate mortgage_monthly in draft whenever offer price / price or params change. */
    function recalcMortgage(d: Property): Property {
        const initialInterest = calcInitialMonthlyInterest(
            d.offer_price ?? d.price,
            d.down_payment_pct ?? 0.20,
            d.mortgage_interest_rate ?? 0.05,
        )
        const monthly = calcMortgage(
            d.offer_price ?? d.price,
            d.down_payment_pct ?? 0.20,
            d.mortgage_interest_rate ?? 0.05,
            d.amortization_years ?? 25,
        )
        return {
            ...d,
            mortgage_monthly: monthly,
            monthly_total: calcMonthlyTotal(monthly, d.property_tax, d.hoa_monthly),
            monthly_cost: calcMonthlyTotal(initialInterest, d.property_tax, d.hoa_monthly),
        }
    }

    function enterLocationEdit() {
        setLocationDraft({ skytrain_station: property.skytrain_station ?? null, skytrain_walk_min: property.skytrain_walk_min ?? null })
        setLocationEditMode(true)
    }

    function cancelLocationEdit() {
        setLocationEditMode(false)
        setLocationDraft(null)
    }

    async function saveLocationEdits() {
        if (!locationDraft || !property) return
        setLocationSaving(true)
        setError(null)
        try {
            const resp = await fetch(`/api/listings/${property.id}/details`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(locationDraft),
            })
            if (!resp.ok) throw new Error(await resp.text())
            const updated: Property = await resp.json()
            setProperty({ ...updated, images: property.images })
            setLocationEditMode(false)
            setLocationDraft(null)
        } catch (err: any) {
            setError(err?.message || String(err))
        } finally {
            setLocationSaving(false)
        }
    }

    function enterFinanceEdit() {
        setFinanceDraft(recalcMortgage({ ...property }))
        setFinanceEditMode(true)
    }

    function cancelFinanceEdit() {
        setFinanceEditMode(false)
        setFinanceDraft(null)
    }

    async function saveFinanceEdits() {
        if (!financeDraft || !property) return
        setFinanceSaving(true)
        setError(null)
        try {
            const resp = await fetch(`/api/listings/${property.id}/details`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(toUserDetails(financeDraft)),
            })
            if (!resp.ok) throw new Error(await resp.text())
            const updated: Property = await resp.json()
            setProperty({ ...updated, images: property.images })
            if (editMode) {
                setDraft(updated)
            }
            setFinanceEditMode(false)
            setFinanceDraft(null)
        } catch (err: any) {
            setError(err?.message || String(err))
        } finally {
            setFinanceSaving(false)
        }
    }

    async function handleSaveEdits() {
        if (!draft || !property) return
        setSaving(true)
        setError(null)
        try {
            const resp = await fetch(`/api/listings/${property.id}/details`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(toUserDetails(draft)),
            })
            if (!resp.ok) throw new Error(await resp.text())
            const updated: Property = await resp.json()
            setProperty({ ...updated, images: property.images })
            setEditMode(false)
            setDraft(null)
        } catch (err: any) {
            setError(err?.message || String(err))
        } finally {
            setSaving(false)
        }
    }

    // ── URL save (right panel) ────────────────────────────────────────────────

    async function saveUrls(): Promise<boolean> {
        setUrlsSaving(true)
        setUrlSaveError(null)
        try {
            const resp = await fetch(`/api/listings/${property.id}/details`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(urlDraft),
            })
            if (!resp.ok) throw new Error(await resp.text())
            const updated: Property = await resp.json()
            setProperty({ ...updated, images: property.images })
            setUrlDraft({ redfin_url: updated.redfin_url, realtor_url: updated.realtor_url, rew_url: updated.rew_url, zillow_url: updated.zillow_url })
            setEditingUrlKey(null)
            return true
        } catch (err: any) {
            setUrlSaveError(err?.message || String(err))
            return false
        } finally {
            setUrlsSaving(false)
        }
    }

    // ── Refresh with preview diff ─────────────────────────────────────────────

    async function handleRefreshPreview() {
        setError(null)
        setRefreshMsg(null)
        // Save any URL edits before refreshing
        const hasChanges = urlDraft.redfin_url !== property.redfin_url ||
            urlDraft.realtor_url !== property.realtor_url ||
            urlDraft.rew_url !== property.rew_url ||
            urlDraft.zillow_url !== property.zillow_url
        if (hasChanges) {
            const ok = await saveUrls()
            if (!ok) return
        }
        setPreviewing(true)
        try {
            const resp = await fetch(`/api/listings/${property.id}/preview`)
            if (!resp.ok) throw new Error(await resp.text())
            const result: PreviewResult = await resp.json()
            const fresh: Property = result.kind === 'status_only'
                ? { ...property, source_status: result.source_status }
                : result.property
            setDiffModal(buildDiff(property, fresh))
        } catch (err: any) {
            setError(err?.message || String(err))
        } finally {
            setPreviewing(false)
        }
    }

    async function applyRefresh() {
        setApplying(true)
        try {
            const resp = await fetch(`/api/listings/${property.id}/refresh`, { method: 'PUT' })
            if (!resp.ok) throw new Error(await resp.text())
            const updated: Property = await resp.json()
            setProperty(updated)
            setTitleDraft(updated.title ?? '')
            setUrlDraft({ redfin_url: updated.redfin_url, realtor_url: updated.realtor_url, rew_url: updated.rew_url, zillow_url: updated.zillow_url })
            setDiffModal(null)
            setRefreshMsg('Property updated successfully')
            setTimeout(() => setRefreshMsg(null), 3000)
            // Reload history
            const histResp = await fetch(`/api/listings/${property.id}/history`)
            if (histResp.ok) setHistory(await histResp.json())
        } catch (err: any) {
            setError(err?.message || String(err))
        } finally {
            setApplying(false)
        }
    }

    // ── Notes ─────────────────────────────────────────────────────────────────

    async function handleNotesSave() {
        setNotesSaving(true)
        const normalizedNotes = replaceEmojiShortcodes(notes)
        setNotes(normalizedNotes)
        setEmojiSuggestions([])
        setEmojiSuggestRange(null)
        try {
            const resp = await fetch(`/api/listings/${property.id}/notes`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ notes: normalizedNotes || null }),
            })
            if (!resp.ok) throw new Error(await resp.text())
        } catch (err: any) {
            setError(err?.message || String(err))
        } finally {
            setNotesSaving(false)
        }
    }

    function refreshEmojiSuggestions(inputValue: string, caretPos: number) {
        const trigger = detectEmojiQuery(inputValue, caretPos)
        if (!trigger) {
            setEmojiSuggestions([])
            setEmojiSuggestRange(null)
            setEmojiSuggestActiveIdx(0)
            return
        }

        const suggestions = buildEmojiSuggestions(trigger.query)
        setEmojiSuggestions(suggestions)
        setEmojiSuggestRange({ start: trigger.start, end: trigger.end })
        setEmojiSuggestActiveIdx(0)
    }

    function insertEmojiSuggestion(suggestion: EmojiSuggestion) {
        if (!emojiSuggestRange) return
        const next = `${notes.slice(0, emojiSuggestRange.start)}${suggestion.emoji}${notes.slice(emojiSuggestRange.end)}`
        const nextCaret = emojiSuggestRange.start + suggestion.emoji.length
        setNotes(next)
        setEmojiSuggestions([])
        setEmojiSuggestRange(null)
        requestAnimationFrame(() => {
            const textarea = notesInputRef.current
            if (!textarea) return
            textarea.focus()
            textarea.setSelectionRange(nextCaret, nextCaret)
        })
    }

    // ── Title (inline) ─────────────────────────────────────────────────────────

    async function handleTitleSave() {
        if (!titleDraft.trim()) return
        const newTitle = titleDraft.trim()
        if (newTitle === property.title) return
        setProperty({ ...property, title: newTitle })
        try {
            const resp = await fetch(`/api/listings/${property.id}/details`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTitle }),
            })
            if (!resp.ok) throw new Error(await resp.text())
            setTitleToast(true)
            setTimeout(() => setTitleToast(false), 4000)
        } catch (err: any) {
            setError(err?.message || String(err))
        }
    }

    // ── Status ────────────────────────────────────────────────────────────────

    async function handleStatusChange(newStatus: StatusOption) {
        const updated = { ...property, status: newStatus }
        setProperty(updated)
        try {
            const resp = await fetch(`/api/listings/${property.id}/details`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(toUserDetails(updated)),
            })
            if (!resp.ok) throw new Error(await resp.text())
        } catch (err: any) {
            setError(err?.message || String(err))
        }
    }

    // ── Delete ────────────────────────────────────────────────────────────────

    async function handleDelete() {
        if (!window.confirm(`Delete "${property.title}"? This cannot be undone.`)) return
        setDeleting(true)
        try {
            const resp = await fetch(`/api/listings/${property.id}/delete`, { method: 'DELETE' })
            if (!resp.ok) throw new Error(await resp.text())
            onAfterDelete?.()
        } catch (err: any) {
            setError(err?.message || String(err))
            setDeleting(false)
        }
    }

    // ── Agent re-review ───────────────────────────────────────────────────────

    async function handleAgentReview() {
        setAgentReviewing(true)
        setAgentReviewError(null)
        try {
            const triggerResp = await fetch(`/api/listings/${property.id}/agent-review/run`, { method: 'POST' })
            if (!triggerResp.ok) throw new Error(await triggerResp.text())

            // Poll until agent_comment changes (or status changes), max ~15s
            const before = property.agent_comment
            let updated: Property | null = null
            for (let i = 0; i < 30; i++) {
                await new Promise(r => setTimeout(r, 500))
                const resp = await fetch(`/api/listings/${property.id}`)
                if (!resp.ok) break
                const p: Property = await resp.json()
                if (p.agent_comment !== before || p.status !== property.status) {
                    updated = p
                    break
                }
            }
            if (updated) {
                setProperty(updated)
            } else {
                setAgentReviewError('Timed out — check backend log')
            }
        } catch (err: any) {
            setAgentReviewError(err?.message || String(err))
        } finally {
            setAgentReviewing(false)
        }
    }

    // ── Image delete ──────────────────────────────────────────────────────────

    async function handleDeleteImage(imageId: number) {
        try {
            const resp = await fetch(`/api/listings/${property.id}/images/${imageId}`, { method: 'DELETE' })
            if (!resp.ok) throw new Error(await resp.text())
            setProperty({ ...property, images: property.images.filter(img => img.id !== imageId) })
        } catch (err: any) {
            setError(err?.message || String(err))
        }
    }

    // ── Render ────────────────────────────────────────────────────────────────

    const address = [property.street_address, property.city, property.region, property.postal_code]
        .filter(Boolean).join(', ')

    // What to render: draft in edit mode, property otherwise
    const p = editMode && draft ? draft : property
    const finance = financeEditMode && financeDraft ? financeDraft : property
    const financeBasePrice = finance.offer_price ?? finance.price
    const initialMonthlyInterest = calcInitialMonthlyInterest(
        financeBasePrice,
        finance.down_payment_pct ?? 0.20,
        finance.mortgage_interest_rate ?? 0.05,
    )
    const monthlyTotalDerived = calcMonthlyTotal(finance.mortgage_monthly, finance.property_tax, finance.hoa_monthly)
    const monthlyCost = calcMonthlyTotal(initialMonthlyInterest, finance.property_tax, finance.hoa_monthly)
    const taxMonthly = finance.property_tax != null ? Math.floor(finance.property_tax / 12) : 0
    const hoaMonthly = finance.hoa_monthly ?? 0
    const effectiveOfferPrice = finance.offer_price ?? finance.price
    const hasCustomOfferPrice = finance.offer_price != null && finance.price != null && finance.offer_price !== finance.price
    const hasUrlChanges = urlDraft.redfin_url !== property.redfin_url ||
        urlDraft.realtor_url !== property.realtor_url ||
        urlDraft.rew_url !== property.rew_url ||
        urlDraft.zillow_url !== property.zillow_url
    const externalUrlRows: Array<{ key: 'redfin_url' | 'realtor_url' | 'rew_url' | 'zillow_url'; label: string; placeholder: string }> = [
        { key: 'redfin_url', label: 'Redfin', placeholder: 'https://www.redfin.ca/…' },
        { key: 'realtor_url', label: 'Realtor.ca', placeholder: 'https://www.realtor.ca/…' },
        { key: 'rew_url', label: 'rew.ca', placeholder: 'https://www.rew.ca/properties/…' },
        { key: 'zillow_url', label: 'Zillow', placeholder: 'https://www.zillow.com/homedetails/…' },
    ]
    const totalParkingSpace =
        p.parking_total ?? (
            p.parking_garage != null || p.parking_carport != null || p.parking_pad != null
                ? (p.parking_garage ?? 0) + (p.parking_carport ?? 0) + (p.parking_pad ?? 0)
                : null
        )
    const monthlyTotalParts = [
        `${moneyPart(finance.mortgage_monthly)} mortgage`,
        `${moneyPart(taxMonthly)} property tax`,
        ...(hoaMonthly > 0 ? [`${moneyPart(hoaMonthly)} HOA`] : []),
    ]
    const monthlyCostParts = [
        `${moneyPart(initialMonthlyInterest)} initial interest`,
        `${moneyPart(taxMonthly)} property tax`,
        ...(hoaMonthly > 0 ? [`${moneyPart(hoaMonthly)} HOA`] : []),
    ]
    const monthlyTotalBreakdown = monthlyTotalParts.join(' + ')
    const monthlyCostBreakdown = monthlyCostParts.join(' + ')

    // Helper to wrap a field: in edit mode shows input, else shows static value
    function Field({ label, viewVal, editEl }: {
        label: string; viewVal: string; editEl?: React.ReactNode
    }) {
        if (editMode && editEl) return <>{editEl}</>
        return (
            <div className="tracked-field">
                <label>{label}</label>
                <span className="tracked-value">{viewVal}</span>
            </div>
        )
    }

    return (
        <div className={`property-detail${embedded ? ' property-detail--embedded' : ''}`}>
                {diffModal !== null && (
                    <RefreshDiffModal
                        diffs={diffModal}
                        onApply={applyRefresh}
                        onCancel={() => setDiffModal(null)}
                        applying={applying}
                    />
                )}

                {error && <div className="message error">{error}</div>}
                {refreshMsg && <div className="message success">{refreshMsg}</div>}

                {lightboxOpen && property.images.length > 0 && (
                    <div className="modal-overlay" onClick={() => setLightboxOpen(false)}>
                        <div className="lightbox-panel" onClick={e => e.stopPropagation()}>
                            <div className="lightbox-header">
                                <button className="lightbox-close" onClick={() => setLightboxOpen(false)}>✕</button>
                                <span className="lightbox-title">{property.title}</span>
                                <span className="lightbox-count">{property.images.length} photos</span>
                            </div>
                            <div className="lightbox-body">
                                <div className="lightbox-thumbs" ref={thumbsRef}>
                                    {property.images.map((img, i) => (
                                        <img
                                            key={img.id}
                                            src={img.url}
                                            alt={`${i + 1}`}
                                            className={`lightbox-thumb${activeIdx === i ? ' active' : ''}`}
                                            onClick={() => goTo(i)}
                                        />
                                    ))}
                                </div>
                                <div
                                    className="lightbox-scroll"
                                    ref={scrollRef}
                                    onScroll={() => {
                                        if (programmaticScroll.current) return
                                        const container = scrollRef.current
                                        if (!container) return
                                        const items = container.querySelectorAll<HTMLElement>('.lightbox-item')
                                        let closest = 0
                                        let minDist = Infinity
                                        items.forEach((el, i) => {
                                            const dist = Math.abs(el.getBoundingClientRect().top - container.getBoundingClientRect().top)
                                            if (dist < minDist) { minDist = dist; closest = i }
                                        })
                                        if (closest !== activeIdx) {
                                            setActiveIdx(closest)
                                            const thumb = thumbsRef.current?.querySelectorAll<HTMLElement>('.lightbox-thumb')[closest]
                                            thumb?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
                                        }
                                    }}
                                >
                                    {property.images.map((img, i) => (
                                        <div key={img.id} className="lightbox-item">
                                            <img src={img.url} alt={`${property.title} — ${i + 1}`} className="lightbox-img" />
                                            <span className="lightbox-caption">{i + 1} / {property.images.length}</span>
                                            <span className="lightbox-date">{formatImgDate(img.created_at)}</span>
                                            <button
                                                className="lightbox-delete-btn"
                                                title="Delete image"
                                                onClick={e => { e.stopPropagation(); handleDeleteImage(img.id) }}
                                            >✕</button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                <div className="detail-images">
                    {property.images.length > 0 ? (
                        <div className="image-grid" onClick={() => setLightboxOpen(true)}>
                            {property.images.slice(0, 3).map((img, i) => (
                                <div
                                    key={img.id}
                                    className={`image-grid-cell${i === 0 ? ' image-grid-main' : ''}`}
                                >
                                    <img src={img.url} alt={property.title} className="image-grid-img" />
                                    {i === 2 && property.images.length > 3 && (
                                        <div className="image-grid-more">+{property.images.length - 3}</div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="no-image">No images available</div>
                    )}
                </div>

                <div className="detail-body">
                    <div className="detail-content">
                        <div className="detail-header">
                            <input
                                className="title-input"
                                value={titleDraft}
                                onChange={e => setTitleDraft(e.target.value)}
                                onBlur={handleTitleSave}
                                placeholder="(no title)"
                                aria-label="Property title"
                            />
                            <div className="detail-price">{formatPriceFull(p.price, p.price_currency)}</div>
                        </div>

                        {address && <div className="detail-address">{address}</div>}

                        {property.description && (
                            <div className="detail-description">
                                <h3>Description</h3>
                                <p>{property.description}</p>
                            </div>
                        )}

                        <div className="tracked-details">
                            <div className="tracked-details-header">
                                <h3>Details</h3>
                                {!editMode ? (
                                    <button className="edit-btn" onClick={enterEdit}>Edit</button>
                                ) : (
                                    <div className="detail-edit-actions">
                                        <button className="save-btn" onClick={handleSaveEdits} disabled={saving}>
                                            {saving ? 'Saving…' : 'Save'}
                                        </button>
                                        <button className="cancel-btn" onClick={cancelEdit} disabled={saving}>Cancel</button>
                                    </div>
                                )}
                            </div>

                            <div className="tracked-group">
                                <h4>Property</h4>
                                <div className="tracked-fields">
                                    {(p.bedrooms != null || editMode) && (
                                        <Field label={LABELS.BEDROOMS} viewVal={numLabel(p.bedrooms)}
                                            editEl={<NumInput label={LABELS.BEDROOMS} value={draft?.bedrooms ?? null} onChange={v => setDraftField('bedrooms', v)} />} />
                                    )}
                                    {(p.bathrooms != null || editMode) && (
                                        <Field label={LABELS.BATHROOMS} viewVal={numLabel(p.bathrooms)}
                                            editEl={<NumInput label={LABELS.BATHROOMS} value={draft?.bathrooms ?? null} onChange={v => setDraftField('bathrooms', v)} />} />
                                    )}
                                    {(p.year_built != null || editMode) && (
                                        <Field label={LABELS.YEAR_BUILT} viewVal={numLabel(p.year_built)}
                                            editEl={<NumInput label={LABELS.YEAR_BUILT} value={draft?.year_built ?? null} onChange={v => setDraftField('year_built', v)} />} />
                                    )}
                                    {(p.sqft != null || editMode) && (
                                        <Field label={LABELS.LIVING_AREA} viewVal={numLabel(p.sqft, ' sqft')}
                                            editEl={<NumInput label={LABELS.LIVING_AREA} value={draft?.sqft ?? null} onChange={v => setDraftField('sqft', v)} />} />
                                    )}
                                    {(p.land_sqft != null || editMode) && (
                                        <Field label={LABELS.LOT_SIZE} viewVal={numLabel(p.land_sqft, ' sqft')}
                                            editEl={<NumInput label={LABELS.LOT_SIZE} value={draft?.land_sqft ?? null} onChange={v => setDraftField('land_sqft', v)} />} />
                                    )}
                                </div>
                            </div>

                            <div className="tracked-group">
                                <h4>Parking</h4>
                                <div className="tracked-fields">
                                    <Field label={LABELS.TOTAL_PARKING} viewVal={numLabel(totalParkingSpace)} />
                                    <Field label={LABELS.GARAGE} viewVal={numLabel(p.parking_garage)}
                                        editEl={<NumInput label={LABELS.GARAGE} value={draft?.parking_garage ?? null} onChange={v => setDraftField('parking_garage', v)} />} />
                                    {(p.parking_carport != null || editMode) && (
                                        <Field label={LABELS.CARPORT} viewVal={numLabel(p.parking_carport)}
                                            editEl={<NumInput label={LABELS.CARPORT} value={draft?.parking_carport ?? null} onChange={v => setDraftField('parking_carport', v)} />} />
                                    )}
                                    {(p.parking_pad != null || editMode) && (
                                        <Field label={LABELS.PARKING_PAD} viewVal={numLabel(p.parking_pad)}
                                            editEl={<NumInput label={LABELS.PARKING_PAD} value={draft?.parking_pad ?? null} onChange={v => setDraftField('parking_pad', v)} />} />
                                    )}
                                </div>
                            </div>



                            {(editMode || p.radiant_floor_heating != null || p.ac != null) && (
                                <div className="tracked-group">
                                    <h4>Features</h4>
                                    <div className="tracked-fields">
                                        {(p.radiant_floor_heating != null || editMode) && (
                                            <Field label={LABELS.RADIANT_FLOOR_HEATING} viewVal={boolLabel(p.radiant_floor_heating)}
                                                editEl={<BoolSelect label={LABELS.RADIANT_FLOOR_HEATING} value={draft?.radiant_floor_heating ?? null} onChange={v => setDraftField('radiant_floor_heating', v)} />} />
                                        )}
                                        {(p.ac != null || editMode) && (
                                            <Field label={LABELS.AIR_CONDITIONING} viewVal={boolLabel(p.ac)}
                                                editEl={<BoolSelect label={LABELS.AIR_CONDITIONING} value={draft?.ac ?? null} onChange={v => setDraftField('ac', v)} />} />
                                        )}
                                    </div>
                                </div>
                            )}

                            {(editMode || p.school_elementary != null || p.school_middle != null || p.school_secondary != null) && (
                                <div className="tracked-group">
                                    <h4>Nearby Schools <span className="school-source-note">(Fraser Institute rating /10)</span></h4>
                                    <div className="tracked-fields">
                                        {(p.school_elementary != null || editMode) && (
                                            <div className="tracked-field">
                                                <label>{LABELS.SCHOOL_ELEMENTARY}</label>
                                                {editMode ? (
                                                    <div className="school-edit-row">
                                                        <input className="edit-input" value={draft?.school_elementary ?? ''} onChange={e => setDraftField('school_elementary', e.target.value || null)} placeholder="School name" />
                                                        <input className="edit-input edit-rating" type="number" min={0} max={10} step={0.1} value={draft?.school_elementary_rating ?? ''} onChange={e => setDraftField('school_elementary_rating', e.target.value ? Number(e.target.value) : null)} placeholder="Rating" />
                                                    </div>
                                                ) : (
                                                    <span className="tracked-value school-entry">
                                                        {p.school_elementary ?? '—'}
                                                        {p.school_elementary_rating != null && <span className="school-rating">{p.school_elementary_rating.toFixed(1)}</span>}
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                        {(p.school_middle != null || editMode) && (
                                            <div className="tracked-field">
                                                <label>{LABELS.SCHOOL_MIDDLE}</label>
                                                {editMode ? (
                                                    <div className="school-edit-row">
                                                        <input className="edit-input" value={draft?.school_middle ?? ''} onChange={e => setDraftField('school_middle', e.target.value || null)} placeholder="School name" />
                                                        <input className="edit-input edit-rating" type="number" min={0} max={10} step={0.1} value={draft?.school_middle_rating ?? ''} onChange={e => setDraftField('school_middle_rating', e.target.value ? Number(e.target.value) : null)} placeholder="Rating" />
                                                    </div>
                                                ) : (
                                                    <span className="tracked-value school-entry">
                                                        {p.school_middle ?? '—'}
                                                        {p.school_middle_rating != null && <span className="school-rating">{p.school_middle_rating.toFixed(1)}</span>}
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                        {(p.school_secondary != null || editMode) && (
                                            <div className="tracked-field">
                                                <label>{LABELS.SCHOOL_SECONDARY}</label>
                                                {editMode ? (
                                                    <div className="school-edit-row">
                                                        <input className="edit-input" value={draft?.school_secondary ?? ''} onChange={e => setDraftField('school_secondary', e.target.value || null)} placeholder="School name" />
                                                        <input className="edit-input edit-rating" type="number" min={0} max={10} step={0.1} value={draft?.school_secondary_rating ?? ''} onChange={e => setDraftField('school_secondary_rating', e.target.value ? Number(e.target.value) : null)} placeholder="Rating" />
                                                    </div>
                                                ) : (
                                                    <span className="tracked-value school-entry">
                                                        {p.school_secondary ?? '—'}
                                                        {p.school_secondary_rating != null && <span className="school-rating">{p.school_secondary_rating.toFixed(1)}</span>}
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                        </div>

                        <div className="location-card">
                            <div className="tracked-details-header">
                                <h3>Location</h3>
                            </div>
                            <div className="tracked-fields location-fields">
                                <div className="tracked-field"><label>{LABELS.STREET_ADDRESS}</label><span className="tracked-value">{property.street_address ?? '—'}</span></div>
                                <div className="tracked-field"><label>{LABELS.CITY}</label><span className="tracked-value">{property.city ?? '—'}</span></div>
                                <div className="tracked-field"><label>{LABELS.REGION_PROVINCE}</label><span className="tracked-value">{property.region ?? '—'}</span></div>
                                <div className="tracked-field"><label>{LABELS.POSTAL_CODE}</label><span className="tracked-value">{property.postal_code ?? '—'}</span></div>
                            </div>

                            <div className="location-subsection">
                                <div className="tracked-details-header">
                                    <h4>Transit</h4>
                                    {!locationEditMode ? (
                                        <button className="edit-btn" onClick={enterLocationEdit}>Edit</button>
                                    ) : (
                                        <div className="detail-edit-actions">
                                            <button className="save-btn" onClick={saveLocationEdits} disabled={locationSaving}>
                                                {locationSaving ? 'Saving…' : 'Save'}
                                            </button>
                                            <button className="cancel-btn" onClick={cancelLocationEdit} disabled={locationSaving}>Cancel</button>
                                        </div>
                                    )}
                                </div>
                                <div className="tracked-fields">
                                    <div className="tracked-field">
                                        <label>{LABELS.SKYTRAIN_STATION}</label>
                                        {locationEditMode ? (
                                            <input className="edit-input" value={locationDraft?.skytrain_station ?? ''} onChange={e => setLocationDraft(d => d ? { ...d, skytrain_station: e.target.value || null } : d)} />
                                        ) : (
                                            <span className="tracked-value">{property.skytrain_station ?? '—'}</span>
                                        )}
                                    </div>
                                    <div className="tracked-field">
                                        <label>{LABELS.WALK_TIME}</label>
                                        {locationEditMode ? (
                                            <input className="edit-input" type="number" value={locationDraft?.skytrain_walk_min ?? ''} onChange={e => setLocationDraft(d => d ? { ...d, skytrain_walk_min: e.target.value ? Number(e.target.value) : null } : d)} />
                                        ) : (
                                            <span className="tracked-value">{numLabel(property.skytrain_walk_min, ' min')}</span>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {property.lat != null && property.lon != null && (
                                <div className="map-preview">
                                    <iframe
                                        title="Property Location"
                                        src={`https://maps.google.com/maps?q=${property.lat},${property.lon}&z=15&output=embed`}
                                        loading="lazy"
                                        referrerPolicy="no-referrer-when-downgrade"
                                    />
                                </div>
                            )}
                        </div>

                        <div className="offer-finance-card">
                            <div className="tracked-details-header">
                                <h3>Offer, Cost &amp; Finance</h3>
                                {!financeEditMode ? (
                                    <button className="edit-btn" onClick={enterFinanceEdit}>Edit</button>
                                ) : (
                                    <div className="detail-edit-actions">
                                        <button className="save-btn" onClick={saveFinanceEdits} disabled={financeSaving}>
                                            {financeSaving ? 'Saving…' : 'Save'}
                                        </button>
                                        <button className="cancel-btn" onClick={cancelFinanceEdit} disabled={financeSaving}>Cancel</button>
                                    </div>
                                )}
                            </div>

                            <div className="offer-finance-row offer-finance-row-1">
                                <div className="tracked-field">
                                    <label>Target Offer Price <span className="info-icon">ⓘ<span className="info-tooltip">Used as the base for mortgage calculations. Leave blank to use the listing price.</span></span></label>
                                    {financeEditMode ? (
                                        <div className="target-offer-edit-row">
                                            <input
                                                className="edit-input target-offer-input"
                                                type="number"
                                                value={financeDraft?.offer_price ?? ''}
                                                onChange={e => {
                                                    const updated = recalcMortgage({ ...financeDraft!, offer_price: e.target.value ? Number(e.target.value) : null })
                                                    setFinanceDraft(updated)
                                                }}
                                                placeholder="Defaults to listing price"
                                            />
                                            {finance.price != null && (
                                                <span className="offer-price-asking-hint">
                                                    Asking: {formatPriceFull(finance.price, finance.price_currency)}
                                                </span>
                                            )}
                                        </div>
                                    ) : (
                                        <button className="offer-price-btn" onClick={enterFinanceEdit}>
                                            <span className="offer-price-value">
                                                {formatPriceFull(effectiveOfferPrice, finance.price_currency) ?? '—'}
                                            </span>
                                            {hasCustomOfferPrice && (
                                                <span className="offer-price-original">
                                                    {formatPriceFull(finance.price, finance.price_currency)}
                                                </span>
                                            )}
                                        </button>
                                    )}
                                </div>
                            </div>

                            <div className="offer-finance-row offer-finance-row-3">
                                <div className="tracked-field">
                                    <label>{LABELS.DOWN_PAYMENT_PCT}</label>
                                    {financeEditMode ? (
                                        <input
                                            className="edit-input"
                                            type="number"
                                            min={0} max={100} step={1}
                                            value={financeDraft?.down_payment_pct != null ? (financeDraft.down_payment_pct * 100).toFixed(0) : ''}
                                            onChange={e => {
                                                const pct = e.target.value ? Number(e.target.value) / 100 : null
                                                const updated = recalcMortgage({ ...financeDraft!, down_payment_pct: pct })
                                                setFinanceDraft(updated)
                                            }}
                                        />
                                    ) : (
                                        <span className="tracked-value">{finance.down_payment_pct != null ? `${(finance.down_payment_pct * 100).toFixed(0)}%` : '—'}</span>
                                    )}
                                </div>

                                <div className="tracked-field">
                                    <label>{LABELS.MORTGAGE_RATE}</label>
                                    {financeEditMode ? (
                                        <input
                                            className="edit-input"
                                            type="number"
                                            min={0} max={30} step={0.01}
                                            value={financeDraft?.mortgage_interest_rate != null ? (financeDraft.mortgage_interest_rate * 100).toFixed(2) : ''}
                                            onChange={e => {
                                                const rate = e.target.value ? Number(e.target.value) / 100 : null
                                                const updated = recalcMortgage({ ...financeDraft!, mortgage_interest_rate: rate })
                                                setFinanceDraft(updated)
                                            }}
                                        />
                                    ) : (
                                        <span className="tracked-value">{finance.mortgage_interest_rate != null ? `${(finance.mortgage_interest_rate * 100).toFixed(2)}%` : '—'}</span>
                                    )}
                                </div>

                                <div className="tracked-field">
                                    <label>{LABELS.AMORTIZATION_YEARS}</label>
                                    {financeEditMode ? (
                                        <input
                                            className="edit-input"
                                            type="number"
                                            min={1} max={40} step={1}
                                            value={financeDraft?.amortization_years ?? ''}
                                            onChange={e => {
                                                const yrs = e.target.value ? Number(e.target.value) : null
                                                const updated = recalcMortgage({ ...financeDraft!, amortization_years: yrs })
                                                setFinanceDraft(updated)
                                            }}
                                        />
                                    ) : (
                                        <span className="tracked-value">{numLabel(finance.amortization_years, ' yr')}</span>
                                    )}
                                </div>
                            </div>

                            <div className="offer-finance-row offer-finance-row-3">
                                <div className="tracked-field">
                                    <label>{LABELS.PROPERTY_TAX}</label>
                                    {financeEditMode ? (
                                        <input
                                            className="edit-input"
                                            type="number"
                                            value={financeDraft?.property_tax ?? ''}
                                            onChange={e => {
                                                const updated = recalcMortgage({ ...financeDraft!, property_tax: e.target.value ? Number(e.target.value) : null })
                                                setFinanceDraft(updated)
                                            }}
                                        />
                                    ) : (
                                        <span className="tracked-value">{moneyLabel(finance.property_tax)}</span>
                                    )}
                                </div>

                                <div className="tracked-field">
                                    <label>{LABELS.HOA_MONTHLY}</label>
                                    {financeEditMode ? (
                                        <input
                                            className="edit-input"
                                            type="number"
                                            value={financeDraft?.hoa_monthly ?? ''}
                                            onChange={e => {
                                                const updated = recalcMortgage({ ...financeDraft!, hoa_monthly: e.target.value ? Number(e.target.value) : null })
                                                setFinanceDraft(updated)
                                            }}
                                        />
                                    ) : (
                                        <span className="tracked-value">{moneyLabel(finance.hoa_monthly)}</span>
                                    )}
                                </div>

                                <div className="tracked-field offer-finance-spacer" aria-hidden="true" />
                            </div>

                            <div className="offer-finance-row offer-finance-row-3">
                                <div className="tracked-field">
                                    <label>Mortgage (Monthly) <span className="info-icon">ⓘ<span className="info-tooltip">Derived from offer price (or listing price), down payment %, interest rate, and amortization years</span></span></label>
                                    <span className="tracked-value">{moneyLabel(finance.mortgage_monthly)}</span>
                                </div>
                                <div className="tracked-field">
                                    <label>Monthly Total <span className="info-icon">ⓘ<span className="info-tooltip">{monthlyTotalBreakdown}</span></span></label>
                                    <span className="tracked-value">{moneyLabel(monthlyTotalDerived)}</span>
                                </div>
                                <div className="tracked-field">
                                    <label>Monthly Cost <span className="info-icon">ⓘ<span className="info-tooltip">{monthlyCostBreakdown}</span></span></label>
                                    <span className="tracked-value">{moneyLabel(monthlyCost)}</span>
                                </div>
                            </div>

                            <div className="offer-finance-rental">
                                <h4>Rental</h4>
                                <div className="tracked-fields">
                                    <div className="tracked-field">
                                        <label>Has Rental Suite</label>
                                        {financeEditMode ? (
                                            <select className="edit-input" value={financeDraft?.has_rental_suite === null ? '' : financeDraft?.has_rental_suite ? 'true' : 'false'} onChange={e => setFinanceDraft(d => d ? { ...d, has_rental_suite: e.target.value === '' ? null : e.target.value === 'true' } : d)}>
                                                <option value="">—</option>
                                                <option value="true">Yes</option>
                                                <option value="false">No</option>
                                            </select>
                                        ) : (
                                            <span className="tracked-value">{boolLabel(finance.has_rental_suite)}</span>
                                        )}
                                    </div>
                                    {(financeEditMode || finance.has_rental_suite !== false) && (
                                        <div className="tracked-field">
                                            <label>Rental Income (Est.)</label>
                                            {financeEditMode ? (
                                                <input className="edit-input" type="number" value={financeDraft?.rental_income ?? ''} onChange={e => setFinanceDraft(d => d ? { ...d, rental_income: e.target.value ? Number(e.target.value) : null } : d)} />
                                            ) : (
                                                <span className="tracked-value">{moneyLabel(finance.rental_income)}</span>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="notes-panel">
                        <div className="agent-comment right-panel-section">
                            <div className="agent-comment-header">
                                <h3 className="notes-heading">Agent note</h3>
                                <button
                                    className="agent-review-btn"
                                    onClick={handleAgentReview}
                                    disabled={agentReviewing}
                                    title="Re-run agent review"
                                >
                                    {agentReviewing ? '…' : '↻'}
                                </button>
                            </div>
                            <p className="agent-comment-text">
                                {agentReviewing
                                    ? <span className="agent-comment-empty">Reviewing…</span>
                                    : property.agent_comment ?? <span className="agent-comment-empty">—</span>}
                            </p>
                            {agentReviewError && (
                                <p className="agent-review-error">{agentReviewError}</p>
                            )}
                        </div>
                        <div className="status-picker right-panel-section">
                            <h3 className="notes-heading">Status</h3>
                            <div className="status-picker-buttons">
                                {USER_STATUSES.map(s => (
                                    <button
                                        key={s}
                                        className={`status-option-btn${property.status === s ? ' active' : ''}`}
                                        style={property.status === s ? { background: STATUS_COLORS[s], color: '#fff', borderColor: STATUS_COLORS[s] } : {}}
                                        onClick={() => handleStatusChange(s)}
                                    >
                                        {displayStatus(s)}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {searchProfiles.length > 0 && (
                            <div className="search-picker right-panel-section">
                                <h3 className="notes-heading">Search Profile</h3>
                                <select
                                    className="search-picker-select"
                                    value={property.search_profile_id ?? ''}
                                    onChange={e => {
                                        const val = Number(e.target.value)
                                        if (val) handleMoveToSearchProfile(val)
                                    }}
                                >
                                    {searchProfiles.map(s => (
                                        <option key={s.id} value={s.id}>{s.title}</option>
                                    ))}
                                </select>
                            </div>
                        )}

                        <div className="right-panel-section">
                            <h3 className="notes-heading">My Notes</h3>
                            {notesEditing ? (
                                <div className="notes-edit-wrap">
                                    <textarea
                                        ref={notesInputRef}
                                        className="notes-textarea"
                                        value={notes}
                                        onChange={e => {
                                            const next = replaceEmojiShortcodes(e.target.value)
                                            setNotes(next)
                                            refreshEmojiSuggestions(next, e.target.selectionStart ?? next.length)
                                        }}
                                        onClick={e => refreshEmojiSuggestions(notes, (e.target as HTMLTextAreaElement).selectionStart ?? notes.length)}
                                        onKeyUp={e => {
                                            if (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Enter' || e.key === 'Tab' || e.key === 'Escape') {
                                                return
                                            }
                                            refreshEmojiSuggestions(notes, (e.target as HTMLTextAreaElement).selectionStart ?? notes.length)
                                        }}
                                        onKeyDown={e => {
                                            if (emojiSuggestions.length === 0) return
                                            if (e.key === 'ArrowDown') {
                                                e.preventDefault()
                                                setEmojiSuggestActiveIdx(i => (i + 1) % emojiSuggestions.length)
                                                return
                                            }
                                            if (e.key === 'ArrowUp') {
                                                e.preventDefault()
                                                setEmojiSuggestActiveIdx(i => (i - 1 + emojiSuggestions.length) % emojiSuggestions.length)
                                                return
                                            }
                                            if (e.key === 'Enter' || e.key === 'Tab') {
                                                e.preventDefault()
                                                const picked = emojiSuggestions[emojiSuggestActiveIdx] ?? emojiSuggestions[0]
                                                if (picked) insertEmojiSuggestion(picked)
                                                return
                                            }
                                            if (e.key === 'Escape') {
                                                e.preventDefault()
                                                setEmojiSuggestions([])
                                                setEmojiSuggestRange(null)
                                            }
                                        }}
                                        onBlur={() => {
                                            setEmojiSuggestions([])
                                            setEmojiSuggestRange(null)
                                            setNotesEditing(false)
                                            handleNotesSave()
                                        }}
                                        placeholder="Add personal notes… (supports markdown, emoji shortcodes like :warning:)"
                                        disabled={notesSaving}
                                        autoFocus
                                    />
                                    {emojiSuggestions.length > 0 && (
                                        <div className="emoji-suggest" role="listbox" aria-label="Emoji suggestions">
                                            {emojiSuggestions.map((item, idx) => (
                                                <button
                                                    key={`${item.name}-${item.emoji}`}
                                                    type="button"
                                                    className={`emoji-suggest-item${idx === emojiSuggestActiveIdx ? ' active' : ''}`}
                                                    onMouseDown={e => {
                                                        e.preventDefault()
                                                        insertEmojiSuggestion(item)
                                                    }}
                                                    title={`:${item.name}:`}
                                                >
                                                    <span className="emoji-suggest-glyph">{item.emoji}</span>
                                                    <span className="emoji-suggest-name">:{item.name}:</span>
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div
                                    className={`notes-display${notes ? '' : ' notes-display-empty'}`}
                                    onClick={() => setNotesEditing(true)}
                                    title="Click to edit"
                                >
                                    {notes
                                        ? <div dangerouslySetInnerHTML={{ __html: marked(notes) as string }} />
                                        : <span>Add personal notes…</span>
                                    }
                                </div>
                            )}
                            {notesSaving && <div className="notes-saving">Saving…</div>}
                        </div>

                        <div className="source-urls-panel right-panel-section">
                            <div className="source-urls-header">
                                <h3 className="notes-heading">External URLs</h3>
                                <button
                                    className="refresh-btn"
                                    onClick={handleRefreshPreview}
                                    disabled={previewing || editMode || urlsSaving}
                                    title="Preview changes from source (saves URL edits first)"
                                >
                                    {previewing ? '⟳ Checking…' : urlsSaving ? 'Saving…' : '⟳ Refresh'}
                                </button>
                            </div>
                            {(() => {
                                const filledRows = externalUrlRows.filter(({ key }) => urlDraft[key])
                                const hiddenCount = externalUrlRows.length - filledRows.length
                                const visibleRows = urlsExpanded ? externalUrlRows : filledRows
                                return <>
                                    {visibleRows.map(({ key, label, placeholder }) => {
                                        const currentValue = urlDraft[key]
                                        const isEditing = editingUrlKey === key
                                        return (
                                            <div className="source-url-field" key={key}>
                                                <label>{label}</label>
                                                {isEditing ? (
                                                    <div className="source-url-edit-row">
                                                        <input
                                                            className="edit-input"
                                                            type="url"
                                                            value={currentValue ?? ''}
                                                            onChange={e => {
                                                                const raw = e.target.value
                                                                let cleaned = raw
                                                                try {
                                                                    const u = new URL(raw)
                                                                    u.search = ''
                                                                    cleaned = u.toString()
                                                                } catch { /* keep raw while typing */ }
                                                                setUrlDraft(d => ({ ...d, [key]: cleaned || null }))
                                                            }}
                                                            placeholder={placeholder}
                                                        />
                                                        <button
                                                            className="source-url-edit-btn"
                                                            onClick={() => setEditingUrlKey(null)}
                                                            title="Done editing"
                                                            type="button"
                                                        >
                                                            ✓
                                                        </button>
                                                    </div>
                                                ) : (
                                                    <div className="source-url-line">
                                                        {currentValue ? (
                                                            <a className="source-url-link" href={currentValue} target="_blank" rel="noreferrer">
                                                                {currentValue}
                                                            </a>
                                                        ) : (
                                                            <span className="source-url-empty">—</span>
                                                        )}
                                                        <button
                                                            className="source-url-edit-btn"
                                                            onClick={() => setEditingUrlKey(key)}
                                                            title={`Edit ${label} URL`}
                                                            type="button"
                                                        >
                                                            <svg className="source-url-edit-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                                                <path
                                                                    d="M4 20l4.7-1 9.3-9.3a1.4 1.4 0 0 0 0-2l-1.7-1.7a1.4 1.4 0 0 0-2 0L5 15.3 4 20z"
                                                                    stroke="currentColor"
                                                                    strokeWidth="1.8"
                                                                    strokeLinecap="round"
                                                                    strokeLinejoin="round"
                                                                />
                                                                <path
                                                                    d="M13.2 6.8l4 4"
                                                                    stroke="currentColor"
                                                                    strokeWidth="1.8"
                                                                    strokeLinecap="round"
                                                                />
                                                            </svg>
                                                        </button>
                                                    </div>
                                                )}
                                            </div>
                                        )
                                    })}
                                    {!urlsExpanded && hiddenCount > 0 && (
                                        <button className="panel-more-btn" onClick={() => setUrlsExpanded(true)}>
                                            + {hiddenCount} more
                                        </button>
                                    )}
                                    {urlsExpanded && (
                                        <button className="panel-more-btn" onClick={() => { setUrlsExpanded(false); setEditingUrlKey(null) }}>
                                            Show less
                                        </button>
                                    )}
                                </>
                            })()}
                            {urlSaveError && (
                                <div className="message error url-save-error">{urlSaveError}</div>
                            )}
                            {hasUrlChanges && (
                                <button className="save-btn save-urls-btn" onClick={saveUrls} disabled={urlsSaving}>
                                    {urlsSaving ? 'Saving…' : 'Save URLs'}
                                </button>
                            )}
                        </div>

                        {property.open_houses.length > 0 && (
                            <div className="open-houses-panel right-panel-section">
                                <h3 className="notes-heading">Open Houses</h3>
                                <ul className="open-houses-list">
                                    {property.open_houses.map(oh => (
                                        <li key={oh.id} className={`open-house-entry${oh.visited ? ' visited' : ''}`}>
                                            <div className="open-house-times">
                                                <span className="open-house-date">
                                                    {new Date(oh.start_time).toLocaleDateString('en-CA', {
                                                        weekday: 'short', month: 'short', day: 'numeric',
                                                    })}
                                                </span>
                                                <span className="open-house-time">
                                                    {new Date(oh.start_time).toLocaleTimeString('en-CA', {
                                                        hour: 'numeric', minute: '2-digit',
                                                    })}
                                                    {oh.end_time && ` – ${new Date(oh.end_time).toLocaleTimeString('en-CA', {
                                                        hour: 'numeric', minute: '2-digit',
                                                    })}`}
                                                </span>
                                            </div>
                                            <button
                                                className={`open-house-visited-btn${oh.visited ? ' active' : ''}`}
                                                onClick={async () => {
                                                    const next = !oh.visited
                                                    await fetch(`/api/listings/${property!.id}/open-houses/${oh.id}`, {
                                                        method: 'PATCH',
                                                        headers: { 'Content-Type': 'application/json' },
                                                        body: JSON.stringify({ visited: next }),
                                                    })
                                                    setProperty(prev => prev ? {
                                                        ...prev,
                                                        open_houses: prev.open_houses.map(x => x.id === oh.id ? { ...x, visited: next } : x)
                                                    } : prev)
                                                }}
                                            >
                                                {oh.visited ? 'Visited' : 'Mark visited'}
                                            </button>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {history.length > 0 && (
                            <div className="history-panel right-panel-section">
                                <h3 className="notes-heading">Change History</h3>
                                <ul className="history-list">
                                    {(historyExpanded ? history : history.slice(0, 1)).map(entry => (
                                        <li key={entry.id} className="history-entry">
                                            <span className="history-field">{historyFieldLabel(entry.field_name)}</span>
                                            <span className="history-change">
                                                {formatHistoryValue(entry.field_name, entry.old_value)} → {formatHistoryValue(entry.field_name, entry.new_value)}
                                            </span>
                                            <span className="history-date">
                                                {new Date(entry.changed_at).toLocaleDateString('en-CA', {
                                                    month: 'short', day: 'numeric', year: 'numeric',
                                                })}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                                {history.length > 1 && (
                                    <button className="panel-more-btn" onClick={() => setHistoryExpanded(h => !h)}>
                                        {historyExpanded ? 'Show less' : `+ ${history.length - 1} more`}
                                    </button>
                                )}
                            </div>
                        )}

                        <div className="listing-timestamps right-panel-section">
                            <span>Watched since: {new Date(property.created_at).toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
                            <span>Last refreshed: {property.updated_at ? new Date(property.updated_at).toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }) : '—'}</span>
                        </div>

                        <div className="right-panel-section">
                            <button
                                className="delete-btn"
                                onClick={handleDelete}
                                disabled={deleting || editMode}
                                title="Delete this listing"
                            >
                                {deleting ? 'Deleting…' : 'Delete'}
                            </button>
                        </div>
                    </div>
                </div>

                {titleToast && (
                    <div className="title-toast">Title updated</div>
                )}
            </div>
    )
}

// ── Page wrapper ──────────────────────────────────────────────────────────────

export function PropertyDetail() {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const location = useLocation()
    const fromApp = location.key !== 'default'

    const [property, setProperty] = useState<Property | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function load() {
            try {
                setLoading(true)
                const resp = await fetch(`/api/listings/${id}`)
                if (!resp.ok) throw new Error('Property not found')
                setProperty(await resp.json())
            } catch (err: any) {
                setError(err?.message || String(err))
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [id])

    if (loading) return <div className="loading">Loading...</div>
    if (error || !property) return <div className="error-msg">{error ?? 'Property not found'}</div>

    return (
        <>
            <div className="detail-nav">
                <button className="back-btn" onClick={() => fromApp ? navigate(-1) : navigate('/')}>
                    {fromApp ? (
                        <svg width="7" height="12" viewBox="0 0 7 12" fill="none" aria-hidden="true"><path d="M6 1L1 6l5 5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" /></svg>
                    ) : (
                        <svg width="13" height="12" viewBox="0 0 13 12" fill="none" aria-hidden="true"><path d="M1 5.5L6.5 1 12 5.5V11H8.5V8H4.5v3H1V5.5Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" /></svg>
                    )}
                    {fromApp ? 'Back' : 'Home'}
                </button>
                <span className="detail-nav-title" title={property.title}>{property.title}</span>
            </div>
            <PropertyDetailContent
                initialProperty={property}
                onAfterDelete={() => navigate('/')}
            />
        </>
    )
}
