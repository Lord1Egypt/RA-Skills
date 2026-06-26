const PRODUCTION_API_BASE_URL = 'https://api.asgcard.dev'

export interface CreationTierPrice {
  loadAmount: number
  issuanceFee: number
  topUpFee: number
  serviceFee: number
  totalCost: number
  endpoint: string
}

export interface FundingTierPrice {
  fundAmount: number
  topUpFee: number
  serviceFee: number
  totalCost: number
  endpoint: string
}

export interface LivePricingData {
  creationTiers: CreationTierPrice[]
  fundingTiers: FundingTierPrice[]
}

interface PricingApiResponse {
  creation?: {
    tiers?: unknown[]
  }
  funding?: {
    tiers?: unknown[]
  }
}

const normalizeBaseUrl = (baseUrl: string): string => baseUrl.replace(/\/+$/, '')
const PRICING_REQUEST_TIMEOUT_MS = 3000

const toNumber = (value: unknown): number | null => {
  const num = typeof value === 'number' ? value : Number(value)
  return Number.isFinite(num) ? num : null
}

const toNonEmptyString = (value: unknown): string | null => {
  if (typeof value !== 'string') return null
  const trimmed = value.trim()
  return trimmed.length > 0 ? trimmed : null
}

const parseCreationTier = (raw: unknown): CreationTierPrice | null => {
  if (!raw || typeof raw !== 'object') return null
  const tier = raw as Record<string, unknown>

  const loadAmount = toNumber(tier.loadAmount)
  const issuanceFee = toNumber(tier.issuanceFee)
  const topUpFee = toNumber(tier.topUpFee)
  const serviceFee = toNumber(tier.ourFee ?? tier.serviceFee)
  const totalCost = toNumber(tier.totalCost)
  const endpoint = toNonEmptyString(tier.endpoint)

  if (
    loadAmount === null ||
    issuanceFee === null ||
    topUpFee === null ||
    serviceFee === null ||
    totalCost === null ||
    endpoint === null
  ) {
    return null
  }

  return {
    loadAmount,
    issuanceFee,
    topUpFee,
    serviceFee,
    totalCost,
    endpoint,
  }
}

const parseFundingTier = (raw: unknown): FundingTierPrice | null => {
  if (!raw || typeof raw !== 'object') return null
  const tier = raw as Record<string, unknown>

  const fundAmount = toNumber(tier.fundAmount)
  const topUpFee = toNumber(tier.topUpFee)
  const serviceFee = toNumber(tier.ourFee ?? tier.serviceFee)
  const totalCost = toNumber(tier.totalCost)
  const endpoint = toNonEmptyString(tier.endpoint)

  if (
    fundAmount === null ||
    topUpFee === null ||
    serviceFee === null ||
    totalCost === null ||
    endpoint === null
  ) {
    return null
  }

  return {
    fundAmount,
    topUpFee,
    serviceFee,
    totalCost,
    endpoint,
  }
}

const getPricingCandidates = (): string[] => {
  const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL
  const configuredPricingUrl = configuredBaseUrl
    ? `${normalizeBaseUrl(configuredBaseUrl)}/pricing`
    : null
  const candidates: string[] = []

  const isLocal =
    typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')

  if (isLocal) {
    // Local development: prefer explicitly configured API origin, otherwise localhost API.
    if (configuredPricingUrl) {
      candidates.push(configuredPricingUrl)
    } else {
      candidates.push('http://localhost:3000/pricing')
    }
  } else {
    // In production / deployed previews, prefer same-origin rewrite first.
    candidates.push('/api/pricing')
    if (configuredPricingUrl) {
      candidates.push(configuredPricingUrl)
    } else {
      candidates.push(`${PRODUCTION_API_BASE_URL}/pricing`)
    }
  }

  return [...new Set(candidates)]
}

export const fetchLivePricingData = async (): Promise<LivePricingData | null> => {
  const candidates = getPricingCandidates()

  for (const endpoint of candidates) {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), PRICING_REQUEST_TIMEOUT_MS)
      let response: Response
      try {
        response = await fetch(endpoint, {
          headers: {
            Accept: 'application/json',
          },
          signal: controller.signal,
        })
      } finally {
        clearTimeout(timeoutId)
      }

      if (!response.ok) continue

      const payload = (await response.json()) as PricingApiResponse
      const creationRaw = Array.isArray(payload?.creation?.tiers) ? payload.creation.tiers : []
      const fundingRaw = Array.isArray(payload?.funding?.tiers) ? payload.funding.tiers : []

      const creationTiers = creationRaw
        .map(parseCreationTier)
        .filter((tier): tier is CreationTierPrice => tier !== null)

      const fundingTiers = fundingRaw
        .map(parseFundingTier)
        .filter((tier): tier is FundingTierPrice => tier !== null)

      if (creationTiers.length === 0 && fundingTiers.length === 0) {
        continue
      }

      return { creationTiers, fundingTiers }
    } catch {
      // Try next endpoint candidate.
    }
  }

  return null
}
