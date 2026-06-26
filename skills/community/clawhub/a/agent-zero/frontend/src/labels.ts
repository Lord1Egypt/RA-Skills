export const LABELS = {
  // Identity
  TITLE: 'Title',
  PRICE: 'Price',

  // Location
  ADDRESS: 'Address',
  STREET_ADDRESS: 'Street Address',
  CITY: 'City',
  REGION: 'Region',
  REGION_PROVINCE: 'Region / Province',
  POSTAL_CODE: 'Postal Code',

  // Property
  BEDROOMS: 'Bedrooms',
  BATHROOMS: 'Bathrooms',
  LIVING_AREA: 'Living Area',
  LOT_SIZE: 'Lot Size',
  YEAR_BUILT: 'Year Built',

  // Parking
  TOTAL_PARKING: 'Total Parking Space',
  GARAGE: 'Garage',
  CARPORT: 'Carport',
  PARKING_PAD: 'Parking Pad',

  // Features
  RADIANT_FLOOR_HEATING: 'Radiant Floor Heating',
  AIR_CONDITIONING: 'Air Conditioning',

  // Schools
  SCHOOL_ELEMENTARY: 'Elementary',
  SCHOOL_MIDDLE: 'Middle',
  SCHOOL_SECONDARY: 'Secondary',

  // Transit
  SKYTRAIN_STATION: 'Closest Skytrain Station',
  WALK_TIME: 'Walk Time (Min)',

  // Finance
  PROPERTY_TAX: 'Property Tax (Annual)',
  HOA_MONTHLY: 'HOA / Strata (Monthly)',
  DOWN_PAYMENT_PCT: 'Down Payment %',
  MORTGAGE_RATE: 'Mortgage Rate %',
  AMORTIZATION_YEARS: 'Amortization (Years)',
}

export type LabelKey = keyof typeof LABELS
