export const STATUS_OPTIONS = ['Buyable', 'Interested', 'Pass', 'HumanReview', 'AgentPending', 'AgentSkip'] as const
export type StatusOption = typeof STATUS_OPTIONS[number]

// Statuses available for the user to set manually.
export const USER_STATUSES: readonly StatusOption[] = ['Buyable', 'Interested', 'Pass'] as const

// HumanReview is set by the agent; the human acts by moving to Interested/Buyable/Pass.
export const HUMAN_PENDING_STATUS: StatusOption = 'HumanReview'

// human‑readable labels shown in the UI; keeps the underlying value
// (`Buyable`) unchanged so the backend/data is unaffected.
export const STATUS_DISPLAY: Record<StatusOption, string> = {
  Buyable: 'Candidate',
  Interested: 'Interested',
  Pass: 'Pass',
  HumanReview: 'Review',
  AgentPending: 'Analyzing…',
  AgentSkip: 'Skipped',
}

export const STATUS_COLORS: Record<string, string> = {
  HumanReview: '#d97706',
  Interested: '#0369a1',
  Buyable: '#16a34a',
  Pass: '#9ca3af',
  AgentPending: '#6b7280',
  AgentSkip: '#d1d5db',
}

/**
 * User‑facing text for a status value.  Use wherever a label is rendered.
 *
 * The argument is the raw value (from the API or a constant); this returns the
 * corresponding display string. If the value is unrecognized we just return it
 * verbatim to avoid breaking anything.
 */
export function displayStatus(s: string | null | undefined): string {
  if (s == null) return ''
  return STATUS_DISPLAY[s as StatusOption] ?? s
}
