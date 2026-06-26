// Hand-maintained types matching the Rust backend models.
//
// The generated reference types in frontend/src/bindings/ are auto-updated by
// `cargo test` in the backend. When you add or remove fields from a Rust model,
// the corresponding file in bindings/ will change in the git diff — that is your
// signal to update this file too.
//
// Note: bindings/ uses bigint for i64 (Rust-accurate) but this file uses number
// (correct for JSON API values that are always within JS Number range).

import type { StatusOption } from './constants'

export type OpenHouse = {
  id: number
  listing_id: number
  start_time: string
  end_time: string | null
  visited: boolean
  created_at: string
}

export type ImageEntry = {
  id: number
  url: string
  created_at: string
}

export type SearchProfile = {
  id: number
  title: string
  description: string
  position: number
  created_at: string
  updated_at: string | null
  listing_count: number
}

export type Property = {
  id: number
  search_profile_id: number | null
  redfin_url: string | null
  realtor_url: string | null
  rew_url: string | null
  zillow_url: string | null
  title: string
  description: string
  price: number | null
  price_currency: string | null
  offer_price: number | null
  street_address: string | null
  city: string | null
  region: string | null
  postal_code: string | null
  country: string | null
  bedrooms: number | null
  bathrooms: number | null
  sqft: number | null
  year_built: number | null
  lat: number | null
  lon: number | null
  images: ImageEntry[]
  open_houses: OpenHouse[]
  created_at: string
  updated_at: string | null
  notes: string | null
  parking_garage: number | null
  parking_total: number | null
  parking_carport: number | null
  parking_pad: number | null
  land_sqft: number | null
  property_tax: number | null
  skytrain_station: string | null
  skytrain_walk_min: number | null
  radiant_floor_heating: boolean | null
  ac: boolean | null
  down_payment_pct: number | null
  mortgage_interest_rate: number | null
  amortization_years: number | null
  mortgage_monthly: number | null
  hoa_monthly: number | null
  monthly_total: number | null
  monthly_cost: number | null
  has_rental_suite: boolean | null
  rental_income: number | null
  status: StatusOption
  school_elementary: string | null
  school_elementary_rating: number | null
  school_middle: string | null
  school_middle_rating: number | null
  school_secondary: string | null
  school_secondary_rating: number | null
  property_type: string | null
  listed_date: string | null
  mls_number: string | null
  laundry_in_unit: boolean | null
  source_status: string | null
  agent_comment: string | null
}