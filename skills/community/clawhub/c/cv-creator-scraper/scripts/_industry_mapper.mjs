// Industry category mapper module
// Converts between category names (Chinese/English) and category IDs

import { readFileSync } from 'node:fs';

// Industry tree data structure (from industry-categories.md)
const fallbackIndustryTree = [
  {
    value: '19',
    label: 'Games',
    labelCn: '游戏',
    children: [
      {
        value: '19006',
        label: 'Shooter',
        children: [{ value: '19006001', label: 'Shooter' }],
      },
      {
        value: '19001',
        label: 'MOBA',
        children: [{ value: '19001001', label: 'MOBA' }],
      },
      {
        value: '19012',
        label: 'Strategy & Battle',
        children: [
          { value: '19012003', label: 'PvP' },
          { value: '19012004', label: 'Strategy Survival' },
          { value: '19012002', label: 'Card Battle' },
          { value: '19012001', label: 'Others' },
        ],
      },
      {
        value: '19004',
        label: 'Sports & Racing',
        children: [
          { value: '19004001', label: 'Sports' },
          { value: '19004003', label: 'Racing' },
          { value: '19004002', label: 'Others' },
        ],
      },
      {
        value: '19005',
        label: 'Action',
        children: [
          { value: '19005004', label: 'Fighting' },
          { value: '19005002', label: 'Action Adventure' },
          { value: '19005003', label: 'Platformer' },
          { value: '19005001', label: 'Others' },
        ],
      },
      {
        value: '19013',
        label: 'Role-Playing',
        children: [
          { value: '19013002', label: 'RPG' },
          { value: '19013004', label: 'Open World' },
          { value: '19013001', label: 'MMORPG' },
          { value: '19013003', label: 'Others' },
        ],
      },
      {
        value: '19009',
        label: 'Simulation & Management',
        children: [{ value: '19009001', label: 'Simulation & Management' }],
      },
      {
        value: '19003',
        label: 'Casual & Social',
        children: [
          { value: '19003003', label: 'Puzzle & Casual' },
          { value: '19003002', label: 'Party & Social' },
          { value: '19003001', label: 'Others' },
        ],
      },
      {
        value: '19014',
        label: 'Rhythm',
        children: [{ value: '19014001', label: 'Rhythm' }],
      },
      {
        value: '19007',
        label: 'Horror & Mystery',
        children: [{ value: '19007001', label: 'Horror & Mystery' }],
      },
      {
        value: '19002',
        label: 'Anime',
        children: [{ value: '19002001', label: 'Anime' }],
      },
      {
        value: '19008',
        label: 'Text Adventure',
        children: [{ value: '19008001', label: 'Text Adventure' }],
      },
      {
        value: '19010',
        label: 'Sandbox',
        children: [{ value: '19010001', label: 'Sandbox' }],
      },
      {
        value: '19011',
        label: 'Gaming Equipment',
        children: [{ value: '19011001', label: 'Gaming Equipment' }],
      },
    ],
  },
  {
    value: '25',
    label: 'Beauty & Personal Care',
    labelCn: '美妆与个人护理',
    children: [
      {
        value: '25006',
        label: 'Makeup',
        children: [
          { value: '25006004', label: 'Facial Makeup' },
          { value: '25006003', label: 'Eye Makeup' },
          { value: '25006002', label: 'Lip Makeup' },
          { value: '25006001', label: 'Others' },
        ],
      },
      {
        value: '25011',
        label: 'Tattoo',
        children: [{ value: '25011001', label: 'Tattoo' }],
      },
      {
        value: '25012',
        label: 'Nail Art & Tools',
        children: [{ value: '25012001', label: 'Nail Art & Tools' }],
      },
      {
        value: '25003',
        label: 'Makeup Tools & Accessories',
        children: [{ value: '25003001', label: 'Makeup Tools & Accessories' }],
      },
      {
        value: '25002',
        label: 'Wigs',
        children: [{ value: '25002001', label: 'Wigs' }],
      },
      {
        value: '25009',
        label: 'Skincare',
        children: [{ value: '25009001', label: 'Skincare' }],
      },
      {
        value: '25007',
        label: 'Hair Care',
        children: [{ value: '25007001', label: 'Hair Care' }],
      },
      {
        value: '25004',
        label: 'Oral Care',
        children: [{ value: '25004001', label: 'Oral Care' }],
      },
      {
        value: '25013',
        label: 'Body Care',
        children: [{ value: '25013001', label: 'Body Care' }],
      },
      {
        value: '25008',
        label: 'Beauty Devices & Accessories',
        children: [
          { value: '25008001', label: 'Beauty Devices & Accessories' },
        ],
      },
      {
        value: '25005',
        label: 'Feminine Care',
        children: [{ value: '25005001', label: 'Feminine Care' }],
      },
      {
        value: '25010',
        label: "Men's Care",
        children: [{ value: '25010001', label: "Men's Care" }],
      },
      {
        value: '25001',
        label: 'Adult Products',
        children: [{ value: '25001001', label: 'Adult Products' }],
      },
      {
        value: '25014',
        label: 'Perfume',
        children: [{ value: '25014001', label: 'Perfume' }],
      },
    ],
  },
  {
    value: '16',
    label: 'Clothing & Fashion',
    labelCn: '服装与时尚',
    children: [
      {
        value: '16002',
        label: "Women's Clothing",
        children: [{ value: '16002001', label: "Women's Clothing" }],
      },
      {
        value: '16003',
        label: "Men's Clothing",
        children: [{ value: '16003001', label: "Men's Clothing" }],
      },
      {
        value: '16004',
        label: "Kids' Clothing",
        children: [{ value: '16004001', label: "Kids' Clothing" }],
      },
      {
        value: '16007',
        label: 'Footwear',
        children: [{ value: '16007001', label: 'Footwear' }],
      },
      {
        value: '16005',
        label: 'Bags & Luggage',
        children: [{ value: '16005001', label: 'Bags & Luggage' }],
      },
      {
        value: '16008',
        label: 'Jewelry',
        children: [{ value: '16008001', label: 'Jewelry' }],
      },
      {
        value: '16006',
        label: 'Accessories',
        children: [
          { value: '16006006', label: 'Watches' },
          { value: '16006003', label: 'Sunglasses' },
          { value: '16006007', label: 'Belts' },
          { value: '16006005', label: 'Hats' },
          { value: '16006008', label: 'Ties' },
          { value: '16006004', label: 'Hair Accessories' },
          { value: '16006002', label: 'Scarves' },
          { value: '16006001', label: 'Others' },
        ],
      },
      {
        value: '16001',
        label: 'Occasion Wear',
        children: [
          { value: '16001007', label: 'Workplace & Business Meetings' },
          { value: '16001005', label: 'Daily Casual' },
          { value: '16001008', label: 'Sports' },
          { value: '16001002', label: 'Travel & Dating' },
          { value: '16001003', label: 'Weddings & Banquets' },
          { value: '16001006', label: 'Campus' },
          { value: '16001004', label: 'Niche Hobbies' },
          { value: '16001001', label: 'Others' },
        ],
      },
    ],
  },
  {
    value: '24',
    label: 'Technology & Electronics',
    labelCn: '科技数码',
    children: [
      {
        value: '24001',
        label: 'Electronics',
        children: [
          { value: '24001001', label: 'Mobile Phones' },
          { value: '24001002', label: 'Computers' },
          { value: '24001003', label: 'Photography & Video Equipment' },
          { value: '24001004', label: 'VR & AR' },
          { value: '24001005', label: 'Smart Watches & Bands' },
          { value: '24001006', label: 'Headphones' },
          { value: '24001007', label: 'Others' },
        ],
      },
      {
        value: '24002',
        label: 'Digital Accessories',
        children: [
          { value: '24002002', label: 'Mobile Phone Accessories' },
          { value: '24002003', label: 'Computer Accessories' },
          { value: '24002001', label: 'Others' },
        ],
      },
      {
        value: '24003',
        label: 'Technology News',
        children: [{ value: '24003001', label: 'Technology News' }],
      },
    ],
  },
  {
    value: '12',
    label: 'Outdoor & Sports',
    labelCn: '户外与运动',
    children: [
      {
        value: '12001',
        label: 'Fitness',
        children: [
          { value: '12001001', label: 'Aerobic Training' },
          { value: '12001002', label: 'Strength Training' },
          { value: '12001003', label: 'Healthy Recipes' },
          { value: '12001004', label: 'Fitness Equipment' },
          { value: '12001005', label: 'Yoga & Pilates' },
          { value: '12001006', label: 'Others' },
        ],
      },
      {
        value: '12002',
        label: 'Ball Sports',
        children: [
          { value: '12002001', label: 'Basketball' },
          { value: '12002002', label: 'Football' },
          { value: '12002003', label: 'Volleyball' },
          { value: '12002004', label: 'Tennis' },
          { value: '12002005', label: 'Table Tennis' },
          { value: '12002006', label: 'Badminton' },
          { value: '12002007', label: 'Baseball' },
          { value: '12002008', label: 'Rugby' },
          { value: '12002009', label: 'Hockey' },
          { value: '12002010', label: 'Golf' },
          { value: '12002011', label: 'Others' },
        ],
      },
      {
        value: '12003',
        label: 'Running',
        children: [{ value: '12003001', label: 'Running' }],
      },
      {
        value: '12004',
        label: 'Water Sports',
        children: [
          { value: '12004001', label: 'Swimming' },
          { value: '12004002', label: 'Diving' },
          { value: '12004003', label: 'Rowing & Boating' },
          { value: '12004004', label: 'Others' },
        ],
      },
      {
        value: '12005',
        label: 'Ice & Snow Sports',
        children: [
          { value: '12005001', label: 'Skiing' },
          { value: '12005002', label: 'Skating' },
          { value: '12005003', label: 'Others' },
        ],
      },
      {
        value: '12006',
        label: 'Cycling',
        children: [{ value: '12006001', label: 'Cycling' }],
      },
      {
        value: '12007',
        label: 'Combat & Martial Arts',
        children: [{ value: '12007001', label: 'Combat & Martial Arts' }],
      },
      {
        value: '12008',
        label: 'Camping & Gear',
        children: [{ value: '12008001', label: 'Camping & Gear' }],
      },
      {
        value: '12009',
        label: 'Hiking & Mountaineering',
        children: [{ value: '12009001', label: 'Hiking & Mountaineering' }],
      },
      {
        value: '12010',
        label: 'Extreme Sports',
        children: [
          { value: '12010001', label: 'Surfing' },
          { value: '12010002', label: 'Rock Climbing' },
          { value: '12010003', label: 'Skateboarding' },
          { value: '12010004', label: 'Others' },
        ],
      },
    ],
  },
  {
    value: '26',
    label: 'Food & Beverages',
    labelCn: '美食与饮品',
    children: [
      {
        value: '26001',
        label: 'Food',
        children: [{ value: '26001001', label: 'Food' }],
      },
      {
        value: '26002',
        label: 'Beverages',
        children: [
          { value: '26002001', label: 'Coffee' },
          { value: '26002002', label: 'Tea Drinks' },
          { value: '26002003', label: 'Alcoholic Drinks' },
          { value: '26002004', label: 'Others' },
        ],
      },
      {
        value: '26003',
        label: 'Cooking',
        children: [{ value: '26003001', label: 'Cooking' }],
      },
      {
        value: '26004',
        label: 'Food Exploration & Reviews',
        children: [{ value: '26004001', label: 'Food Exploration & Reviews' }],
      },
      {
        value: '26005',
        label: 'Food Live Streaming',
        children: [{ value: '26005001', label: 'Food Live Streaming' }],
      },
    ],
  },
  {
    value: '15',
    label: 'Travel & Lifestyle',
    labelCn: '旅行与生活方式',
    children: [
      {
        value: '15001',
        label: 'Travel',
        children: [
          { value: '15001001', label: 'Travel Guides' },
          { value: '15001002', label: 'Hotel Experiences' },
          { value: '15001003', label: 'Natural Scenery' },
          { value: '15001004', label: 'Cultural Experiences' },
          { value: '15001005', label: 'Others' },
        ],
      },
      {
        value: '15002',
        label: 'Lifestyle',
        children: [{ value: '15002001', label: 'Lifestyle' }],
      },
    ],
  },
];

function loadIndustryTree() {
  try {
    return JSON.parse(
      readFileSync(
        new URL('./influencer_industry_tree.json', import.meta.url),
        'utf8',
      ),
    );
  } catch (error) {
    console.error(
      `[industry-mapper] Failed to load complete industry tree, using fallback tree: ${error.message}`,
    );
    return fallbackIndustryTree;
  }
}

const IndustryTree = loadIndustryTree();

// Build lookup maps
const idToNameMap = new Map();
const nameToIdMap = new Map();
const cnNameToIdMap = new Map();
const childrenByIdMap = new Map();
const normalizedNameToIdMap = new Map();

function normalizeIndustryKey(name) {
  return String(name)
    .normalize('NFKC')
    .trim()
    .toLowerCase()
    .replace(/['']/g, '')
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function registerNormalizedName(name, id) {
  const key = normalizeIndustryKey(name);
  if (key && !normalizedNameToIdMap.has(key)) {
    normalizedNameToIdMap.set(key, id);
  }
}

function buildMaps(nodes, parentPath = []) {
  for (const node of nodes) {
    const { value, label, labelCn, children } = node;
    
    // ID to name mapping
    idToNameMap.set(value, label);
    
    // Name to ID mapping (case-insensitive)
    nameToIdMap.set(label.toLowerCase(), value);
    registerNormalizedName(label, value);
    
    // Chinese name to ID mapping
    if (labelCn) {
      cnNameToIdMap.set(labelCn, value);
      registerNormalizedName(labelCn, value);
      // Auto-extract short form: "美妆与个人护理" -> "美妆"
      const shortCn = extractShortCn(labelCn);
      if (shortCn && shortCn !== labelCn) {
        cnNameToIdMap.set(shortCn, value);
        registerNormalizedName(shortCn, value);
      }
    }
    
    // Recursively process children
    if (children && children.length > 0) {
      childrenByIdMap.set(value, children.map((child) => child.value));
      buildMaps(children, [...parentPath, label]);
    }
  }
}

function extractShortCn(labelCn) {
  // Extract the first segment as short name
  // e.g. "美妆与个人护理" -> "美妆"
  // e.g. "服装与时尚" -> "服装"
  // e.g. "美食与饮品" -> "美食"
  // e.g. "旅行与生活方式" -> "旅行"
  const splitChars = ['与', '&', '和', '及'];
  for (const ch of splitChars) {
    const idx = labelCn.indexOf(ch);
    if (idx > 0) {
      return labelCn.slice(0, idx);
    }
  }
  return null;
}

buildMaps(IndustryTree);

// Additional common aliases (short form -> ID)
const aliasToIdMap = new Map([
  ['美妆', '25'],
  ['游戏', '19'],
  ['服装', '16'],
  ['数码', '24'],
  ['科技', '24'],
  ['户外', '12'],
  ['运动', '12'],
  ['美食', '26'],
  ['旅行', '15'],
  ['生活', '15'],
  ['电竞', '19'],
  ['手游', '19'],
  ['端游', '19'],
  ['护肤', '25009'],
  ['彩妆', '25006'],
  ['穿搭', '16'],
  ['潮牌', '16'],
  ['健身', '12001'],
  ['篮球', '12002'],
  ['足球', '12002'],
]);

// Merge aliases into cnNameToIdMap
for (const [alias, id] of aliasToIdMap) {
  if (!cnNameToIdMap.has(alias)) {
    cnNameToIdMap.set(alias, id);
  }
  registerNormalizedName(alias, id);
}

// Common English aliases/abbreviations → level-1 category ID
const englishAliasMap = new Map([
  ['fashion', '16'],
  ['clothing', '16'],
  ['apparel', '16'],
  ['beauty', '25'],
  ['cosmetics', '25'],
  ['makeup', '25006'],
  ['skincare', '25009'],
  ['haircare', '25007'],
  ['sports', '12'],
  ['fitness', '12001'],
  ['outdoor', '12'],
  ['tech', '24'],
  ['technology', '24'],
  ['electronics', '24001'],
  ['gadgets', '24'],
  ['food', '26'],
  ['cooking', '26003'],
  ['travel', '15'],
  ['lifestyle', '15002'],
  ['gaming', '19'],
  ['games', '19'],
  ['esports', '19'],
  ['entertainment', '5'],
  ['comedy', '5001'],
  ['humor', '5001'],
  ['pets', '9'],
  ['animals', '9'],
  ['home', '10'],
  ['furniture', '10'],
  ['art', '28'],
  ['music', '28'],
  ['education', '6'],
  ['finance', '29'],
  ['business', '29'],
  ['parenting', '1'],
  ['kids', '1'],
  ['baby', '1'],
  ['automotive', '17'],
  ['cars', '17'],
  ['health', '14'],
  ['wellness', '14'],
  ['books', '7'],
  ['reading', '7'],
]);

// Business-friendly aliases and common fuzzy phrases.
const businessAliasMap = new Map([
  ['outfit', '16'],
  ['outfits', '16'],
  ['styling', '16'],
  ['streetwear', '16'],
  ['shoes', '16007001'],
  ['footwear', '16007001'],
  ['bags', '16005001'],
  ['luggage', '16005001'],
  ['watch', '16006006'],
  ['watches', '16006006'],
  ['sunglasses', '16006003'],

  ['personal care', '25'],
  ['make up', '25006'],
  ['beauty tools', '25003'],
  ['skin care', '25009'],
  ['skin-care', '25009'],
  ['hair care', '25007'],
  ['hair-care', '25007'],
  ['oral care', '25004001'],
  ['body care', '25013001'],
  ['nail', '25012001'],
  ['nails', '25012001'],
  ['nail art', '25012001'],
  ['perfume', '25014001'],
  ['fragrance', '25014001'],
  ['fragrances', '25014001'],

  ['gym', '12001'],
  ['workout', '12001'],
  ['yoga', '12001006'],
  ['pilates', '12001006'],
  ['basketball', '12002'],
  ['football', '12002'],
  ['soccer', '12002'],
  ['outdoors', '12'],

  ['digital', '24'],
  ['smart devices', '24'],
  ['smart home', '24003'],
  ['mobile phone', '24001003'],
  ['mobile phones', '24001003'],
  ['phone', '24001003'],
  ['phones', '24001003'],
  ['phone accessories', '24002002'],
  ['mobile accessories', '24002002'],
  ['headphones', '24001007'],
  ['earbuds', '24001007'],
  ['camera', '24001002'],
  ['cameras', '24001002'],
  ['computer', '24001004'],
  ['computers', '24001004'],

  ['cook', '26003'],
  ['recipe', '26003'],
  ['recipes', '26003'],
  ['beverage', '26002'],
  ['beverages', '26002'],
  ['kitchen', '10002'],
  ['kitchenware', '10002001'],
  ['tableware', '10002001'],

  ['e sports', '19'],
  ['e-sports', '19'],
  ['mobile games', '19'],
  ['pc games', '19'],

  ['humour', '5001'],
  ['funny', '5001'],
  ['joke', '5001'],
  ['jokes', '5001'],
  ['meme', '5001'],
  ['memes', '5001'],
  ['prank', '5001'],
  ['pranks', '5001'],

  ['pet', '9'],
  ['pet supplies', '9002'],
  ['pet products', '9002'],
  ['pet food', '9002004'],
  ['pet toys', '9002002'],

  ['home living', '10'],
  ['home and living', '10'],
  ['home decor', '10007'],
  ['home decoration', '10007'],
  ['home appliance', '10008'],
  ['home appliances', '10008'],
  ['household appliance', '10008005'],
  ['household appliances', '10008005'],
  ['home cleaning', '10006'],
  ['house cleaning', '10006'],
  ['household cleaning', '10006'],
  ['cleaning', '10006'],
  ['cleaning products', '10006'],
  ['home org', '10'],
  ['home organization', '10'],
  ['home organising', '10'],
  ['home organizing', '10'],
  ['organization', '10'],
  ['organising', '10'],
  ['organizing', '10'],
  ['storage', '10'],

  ['learning', '6'],
  ['study', '6'],

  ['family', '1'],
  ['mother', '1'],
  ['mom', '1'],
  ['mum', '1'],
  ['maternity', '1002'],
  ['children', '1'],
  ['child', '1'],
  ['baby products', '1002002'],

  ['auto', '17'],
  ['car', '17'],

  ['toys', '20'],
  ['toy', '20'],
  ['kids toys', '20001'],
  ['children toys', '20001'],
  ['childrens toys', '20001'],
  ['educational toys', '20004'],
  ['building blocks', '20005'],
  ['blocks', '20005'],
  ['lego', '20005'],
  ['model toys', '20003'],
  ['collectible toys', '20002'],
]);

for (const [alias, id] of [...englishAliasMap, ...businessAliasMap]) {
  registerNormalizedName(alias, id);
}

/**
 * Get all level-3 (leaf) category IDs below any known category ID.
 * Leaf IDs are returned unchanged.
 * @param {string} categoryId - Any known category ID
 * @returns {string[]} Array of level-3 category IDs
 */
export function getIndustryLeafCodes(categoryId) {
  if (!idToNameMap.has(categoryId)) {
    return [];
  }

  const childIds = childrenByIdMap.get(categoryId);
  if (!childIds?.length) {
    return [categoryId];
  }

  const leafIds = [];
  for (const childId of childIds) {
    leafIds.push(...getIndustryLeafCodes(childId));
  }
  return leafIds;
}

function normalizeIndustryName(name) {
  return String(name).normalize('NFKC').trim().replace(/\s+/g, ' ');
}

function resolveIndustryId(value) {
  const normalized = normalizeIndustryName(value);
  if (!normalized) {
    return null;
  }

  if (isValidCategoryId(normalized)) {
    return normalized;
  }

  return getIndustryIdByName(normalized);
}

function convertSingleToLeafIds(value) {
  const categoryId = resolveIndustryId(value);
  if (!categoryId) {
    return [];
  }

  return getIndustryLeafCodes(categoryId);
}

function unique(values) {
  return [...new Set(values)];
}

function splitIndustryInput(input) {
  if (Array.isArray(input)) {
    return input.flatMap((value) => splitIndustryInput(value));
  }

  return String(input)
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);
}

/**
 * Validate and convert every input item. If any item is unknown, return an
 * empty result so callers fail before sending a partially-filtered request.
 */
export function convertToLeafIds(input) {
  if (!input) return [];

  const parts = splitIndustryInput(input);
  if (parts.length === 0) {
    return [];
  }

  const leafIds = [];
  for (const part of parts) {
    const converted = convertSingleToLeafIds(part);
    if (converted.length === 0) {
      return [];
    }
    leafIds.push(...converted);
  }

  return unique(leafIds);
}

/**
 * Get category ID by name (Chinese or English)
 * @param {string} name - Category name (e.g., "美妆", "Skincare", "Mobile Phones", "Fashion", "Beauty")
 * @returns {string|null} Category ID or null if not found
 */
export function getIndustryIdByName(name) {
  if (!name) return null;

  const normalizedName = normalizeIndustryName(name);
  const normalizedKey = normalizeIndustryKey(normalizedName);
  
  // Try Chinese name first
  if (cnNameToIdMap.has(normalizedName)) {
    return cnNameToIdMap.get(normalizedName);
  }
  if (normalizedNameToIdMap.has(normalizedKey)) {
    return normalizedNameToIdMap.get(normalizedKey);
  }
  const tokenKey = tokenizeIndustryName(normalizedKey).join(' ');
  if (tokenKey && normalizedNameToIdMap.has(tokenKey)) {
    return normalizedNameToIdMap.get(tokenKey);
  }
  
  // Try English name (case-insensitive)
  const lowerName = normalizedName.toLowerCase();
  if (nameToIdMap.has(lowerName)) {
    return nameToIdMap.get(lowerName);
  }
  
  // Try English alias (common short names)
  if (englishAliasMap.has(lowerName)) {
    return englishAliasMap.get(lowerName);
  }
  if (businessAliasMap.has(lowerName)) {
    return businessAliasMap.get(lowerName);
  }
  
  return null;
}

function tokenizeIndustryName(value) {
  return normalizeIndustryKey(value)
    .split(' ')
    .filter((token) => token.length >= 3)
    .filter((token) => !['and', 'the', 'for', 'with', 'kol', 'kols', 'creator', 'creators', 'influencer', 'influencers', 'product', 'products'].includes(token));
}

function levenshteinDistance(a, b) {
  if (a === b) return 0;
  if (!a) return b.length;
  if (!b) return a.length;

  const previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  const current = new Array(b.length + 1);

  for (let i = 1; i <= a.length; i += 1) {
    current[0] = i;
    for (let j = 1; j <= b.length; j += 1) {
      const substitutionCost = a[i - 1] === b[j - 1] ? 0 : 1;
      current[j] = Math.min(
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + substitutionCost,
      );
    }
    previous.splice(0, previous.length, ...current);
  }

  return previous[b.length];
}

function scoreIndustryCandidate(queryKey, candidateKey) {
  if (!queryKey || !candidateKey) return 0;
  if (queryKey === candidateKey) return 1;
  if (candidateKey.includes(queryKey) || queryKey.includes(candidateKey)) return 0.88;

  const queryTokens = tokenizeIndustryName(queryKey);
  const candidateTokens = tokenizeIndustryName(candidateKey);
  if (queryTokens.length > 0 && candidateTokens.length > 0) {
    const overlap = queryTokens.filter((token) => candidateTokens.includes(token)).length;
    if (overlap > 0) {
      return 0.62 + Math.min(overlap / Math.max(queryTokens.length, candidateTokens.length), 1) * 0.24;
    }
  }

  if (queryKey.length >= 5 && candidateKey.length >= 5) {
    const distance = levenshteinDistance(queryKey, candidateKey);
    const ratio = 1 - distance / Math.max(queryKey.length, candidateKey.length);
    if (ratio >= 0.72) {
      return ratio * 0.72;
    }
  }

  return 0;
}

function candidateDisplayName(id) {
  const name = idToNameMap.get(id);
  const leaves = getIndustryLeafCodes(id);
  return {
    id,
    name,
    leaf_count: leaves.length,
  };
}

/**
 * Suggest likely industry categories without converting the request.
 * Used when confidence is too low to safely send a filtered OpenAPI request.
 * @param {string|string[]} input
 * @param {number} limit
 * @returns {{input:string, suggestions:Array<{id:string,name:string,leaf_count:number,score:number}>}[]}
 */
export function suggestIndustryMatches(input, limit = 5) {
  const parts = splitIndustryInput(input);
  return parts.map((part) => {
    const queryKey = normalizeIndustryKey(part);
    const scored = [];

    for (const [candidateKey, id] of normalizedNameToIdMap) {
      const score = scoreIndustryCandidate(queryKey, candidateKey);
      if (score >= 0.5) {
        scored.push({ id, score });
      }
    }

    const uniqueById = new Map();
    for (const item of scored.sort((a, b) => b.score - a.score)) {
      const existing = uniqueById.get(item.id);
      if (!existing || item.score > existing.score) {
        uniqueById.set(item.id, item);
      }
    }

    const suggestions = [...uniqueById.values()]
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map((item) => ({
        ...candidateDisplayName(item.id),
        score: Number(item.score.toFixed(2)),
      }));

    return {
      input: part,
      suggestions,
    };
  });
}

/**
 * Get English category name by ID
 * @param {string} id - Category ID (e.g., "25009001")
 * @returns {string|null} English category name or null if not found
 */
export function getIndustryNameById(id) {
  return idToNameMap.get(id) || null;
}

/**
 * Check if a string is a known category ID.
 * @param {string} str - String to check
 * @returns {boolean} True if valid ID format
 */
export function isValidCategoryId(str) {
  const normalized = String(str).trim();
  return /^\d+$/.test(normalized) && idToNameMap.has(normalized);
}
