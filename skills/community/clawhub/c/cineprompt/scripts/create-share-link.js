#!/usr/bin/env node
/**
 * CinePrompt Share Link Creator
 * 
 * Creates a CinePrompt share link via authenticated RPC or direct insert.
 * 
 * Auth modes (checked in order):
 *   1. --api-key or CINEPROMPT_API_KEY  → RPC (public, requires Pro subscription)
 *   2. CINEPROMPT_SERVICE_KEY           → Direct insert (internal/owner use only)
 * 
 * Usage:
 *   echo '{"fields":{...},"mode":"single"}' | node create-share-link.js --api-key cp_abc123
 *   node create-share-link.js --state '{"fields":{...}}' --api-key cp_abc123
 *   CINEPROMPT_API_KEY=cp_abc123 node create-share-link.js --state-file state.json
 */

const SUPABASE_URL = 'https://jbeuvbsremektkwqmnps.supabase.co';

async function main() {
  const args = process.argv.slice(2);
  let stateJson, promptText, apiKey;

  // Parse args
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--state' && args[i + 1]) {
      stateJson = JSON.parse(args[++i]);
    } else if (args[i] === '--state-file' && args[i + 1]) {
      const fs = require('fs');
      stateJson = JSON.parse(fs.readFileSync(args[++i], 'utf8'));
    } else if (args[i] === '--prompt' && args[i + 1]) {
      promptText = args[++i];
    } else if (args[i] === '--api-key' && args[i + 1]) {
      apiKey = args[++i];
    }
  }

  // Resolve auth
  apiKey = apiKey || process.env.CINEPROMPT_API_KEY;
  const serviceKey = process.env.CINEPROMPT_SERVICE_KEY;

  if (!apiKey && !serviceKey) {
    console.error('Error: No auth. Set --api-key, CINEPROMPT_API_KEY, or CINEPROMPT_SERVICE_KEY.');
    process.exit(1);
  }

  // Read from stdin if no --state
  if (!stateJson) {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const input = Buffer.concat(chunks).toString().trim();
    if (!input) {
      console.error('Error: No state provided. Use --state, --state-file, or pipe JSON to stdin.');
      process.exit(1);
    }
    const parsed = JSON.parse(input);
    if (parsed.state && parsed.prompt) {
      stateJson = parsed.state;
      promptText = promptText || parsed.prompt;
    } else {
      stateJson = parsed;
    }
  }

  if (!promptText) {
    promptText = buildPromptText(stateJson);
  }

  const mode = stateJson.mode || 'single';

  let result;
  if (apiKey) {
    // Authenticated RPC path (public skill)
    result = await createViaRPC(apiKey, promptText, stateJson, mode);
  } else {
    // Direct insert path (internal/owner use)
    result = await createDirect(serviceKey, promptText, stateJson, mode);
  }

  console.log(JSON.stringify(result));
}

async function createViaRPC(apiKey, promptText, stateJson, mode) {
  // Use anon key for PostgREST access; the CinePrompt API key authenticates inside the RPC
  const ANON_KEY = 'sb_publishable_W-tmZXUJsPIwjMBQVeH2bw_VIIS5PWw';
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/create_share_link`, {
    method: 'POST',
    headers: {
      'apikey': ANON_KEY,
      'Authorization': `Bearer ${ANON_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      api_key: apiKey,
      prompt_text: promptText,
      state_json: stateJson,
      share_mode: mode
    })
  });

  if (!res.ok) {
    const err = await res.text();
    console.error('RPC error:', err);
    process.exit(1);
  }

  const data = await res.json();
  return {
    url: data.url,
    shortCode: data.short_code,
    promptText,
    mode
  };
}

async function createDirect(serviceKey, promptText, stateJson, mode) {
  const shortCode = generateShortCode();
  const res = await fetch(`${SUPABASE_URL}/rest/v1/shared_prompts`, {
    method: 'POST',
    headers: {
      'apikey': serviceKey,
      'Authorization': `Bearer ${serviceKey}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=representation'
    },
    body: JSON.stringify({
      short_code: shortCode,
      prompt_text: promptText,
      state_json: stateJson,
      mode: mode
    })
  });

  if (!res.ok) {
    const err = await res.text();
    console.error('Supabase error:', err);
    process.exit(1);
  }

  const data = await res.json();
  return {
    url: `https://cineprompt.io/p/${shortCode}`,
    shortCode,
    promptText,
    mode,
    id: data[0]?.id
  };
}

function generateShortCode() {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let code = '';
  const bytes = require('crypto').randomBytes(6);
  for (let i = 0; i < 6; i++) {
    code += chars[bytes[i] % chars.length];
  }
  return code;
}

/**
 * Build prompt text from state — mirrors CinePrompt's frontend logic.
 * Handles section ordering, field merging, and sentence assembly.
 */
function buildPromptText(state) {
  const fields = state.fields || {};
  
  // Section order (Universal model default)
  const sectionOrder = [
    { section: 'STYLE', fields: ['media_type', 'commercial_type', 'documentary_style', 'animation_style', 'music_video_style', 'social_media_style', 'genre', 'tone', 'format'] },
    { section: 'SUBJECT', fields: ['char_label', 'age_range', 'build', 'hair_style', 'hair_color', 'subject_description', 'wardrobe', 'expression', 'body_language', 'framing', 'creature_category', 'creature_label', 'creature_size', 'creature_body', 'creature_skin', 'creature_description', 'creature_expression', 'creature_framing', 'obj_description', 'obj_material', 'obj_condition', 'obj_scale', 'prod_description', 'prod_material', 'prod_staging', 'prod_condition', 'food_description', 'food_state', 'food_presentation', 'food_texture', 'cloth_description', 'cloth_fabric', 'cloth_presentation', 'cloth_fit', 'art_description', 'art_medium', 'art_setting', 'art_condition', 'botan_description', 'botan_type', 'botan_stage', 'botan_detail', 'veh_type', 'veh_description', 'veh_era', 'veh_condition', 'land_season', 'land_scale', 'abs_description', 'abs_quality', 'abs_movement'] },
    { section: 'ACTIONS', fields: ['movement_type', 'pacing', 'interaction_type', 'action_primary', 'beat_1', 'beat_2', 'beat_3'] },
    { section: 'ENVIRONMENT', fields: ['setting', 'isolation', 'location_type', 'abstract_environment', 'custom_location', 'location', 'env_time', 'weather', 'props', 'env_fg', 'env_mg', 'env_bg'] },
    { section: 'CINEMATOGRAPHY', fields: ['shot_type', 'movement', 'camera_body', 'focal_length', 'lens_brand', 'lens_filter', 'dof', 'lighting_style', 'lighting_type', 'key_light', 'fill_light'] },
    { section: 'PALETTE', fields: ['color_science', 'film_stock', 'color_grade', 'palette_colors', 'skin_tones'] },
    { section: 'SOUND', fields: ['sound_mode', 'voiceover_text', 'sfx_environment', 'sfx_interior', 'sfx_mechanical', 'sfx_dramatic', 'ambient', 'music_genre', 'music_mood', 'music'] }
  ];

  // Natural language join
  const nlJoin = (arr) => {
    if (!Array.isArray(arr)) return arr;
    if (arr.length <= 1) return arr[0] || '';
    return arr.slice(0, -1).join(', ') + ' and ' + arr[arr.length - 1];
  };

  // Media type smart merge
  const mediaSubcatFields = {
    'commercial': 'commercial_type', 'cinematic': 'genre', 'documentary': 'documentary_style',
    'animation': 'animation_style', 'music video': 'music_video_style', 'social media': 'social_media_style'
  };
  const mediaAbsorbed = new Set(['media_type', 'commercial_type', 'documentary_style', 'animation_style', 'music_video_style', 'social_media_style', 'genre']);

  let mediaTypeMerged = null;
  if (fields.media_type) {
    const types = Array.isArray(fields.media_type) ? fields.media_type : [fields.media_type];
    const parts = [];
    for (const mt of types) {
      const subcatField = mediaSubcatFields[mt];
      const subcatVal = subcatField ? fields[subcatField] : null;
      if (subcatVal) {
        if (mt === 'cinematic' && subcatVal) {
          const genreArr = Array.isArray(subcatVal) ? subcatVal : [subcatVal];
          parts.push(`cinematic ${nlJoin(genreArr)}`);
        } else if (Array.isArray(subcatVal)) {
          parts.push(nlJoin(subcatVal));
        } else {
          parts.push(subcatVal);
        }
      } else {
        parts.push(mt);
      }
    }
    mediaTypeMerged = parts.join(' ');
  }

  // Merge rules (simplified — covers the main field pairs)
  const mergeRules = {
    'shot_type': { mergeWith: 'movement', fn: (a, b) => {
      if (a && b) return b === 'static' ? `${a}, locked-off static camera` : `${a} with ${b} camera movement`;
      if (b) return b === 'static' ? 'locked-off static camera' : `${b} camera movement`;
      return a;
    }},
    'setting': { mergeWith: 'location_type', fn: (s, lt) => {
      const custom = fields.custom_location || '';
      let loc = lt && custom ? `${lt}, ${custom}` : (lt || custom || '');
      if (s && loc) return `${s}, ${loc}`;
      return s || loc;
    }},
    'focal_length': { mergeWith: 'lens_brand', fn: (fl, b) => {
      if (fl && b) return `${fl.replace(/ lens$/, '')} ${b}`;
      return fl || b;
    }},
    'lighting_style': { mergeWith: 'lighting_type', fn: (s, t) => {
      if (s && t) return `${s.replace(/ light$/, '').replace(/ lighting$/, '')} ${t}`;
      return s || t;
    }},
    'env_time': { mergeWith: 'weather', fn: (t, w) => {
      if (t && w) return `${t}, ${w}`;
      return t || w;
    }},
    'key_light': { mergeWith: 'fill_light', fn: (k, f) => {
      if (k && f) return `${k}, ${f}`;
      return k || f;
    }},
    'camera_body': { mergeWith: 'color_science', fn: (cam, cs) => {
      if (cam && cs) {
        let profileName = cs.split(' flat log')[0].split(' flat ')[0];
        const brands = ['ARRI', 'Sony', 'RED', 'Canon', 'Panasonic', 'Blackmagic'];
        for (const brand of brands) {
          if (cam.includes(brand) && profileName.startsWith(brand + ' ')) {
            profileName = profileName.slice(brand.length + 1);
            break;
          }
        }
        return `${cam} in ${profileName}, flat log footage, ungraded`;
      }
      return cam || cs;
    }},
    'film_stock': { mergeWith: 'color_grade', fn: (s, g) => {
      if (s && g) return `${s}, ${g}`;
      return s || g;
    }},
    'hair_style': { mergeWith: 'hair_color', fn: (s, c) => {
      if (s && c) return `${s.replace(/ hair$/, '')} ${c.replace(/ hair$/, '')} hair`;
      return s || c;
    }},
    'expression': { mergeWith: 'body_language', fn: (e, b) => {
      if (e && b) return `${e}, ${b}`;
      return e || b;
    }},
    'char_label': { mergeWith: 'age_range', fn: (l, a) => {
      if (l && a) return a.startsWith('in their') ? `${l} ${a}` : `${l}, ${a}`;
      return l || a;
    }},
    'creature_category': { mergeWith: 'creature_label', fn: (c, l) => {
      if (c && l) return `${c}, ${l}`;
      return c || l;
    }},
    'music_genre': { mergeWith: 'music_mood', fn: (g, m) => {
      if (g && m) return `${m.split(',')[0].trim()} ${g}`;
      return g || m;
    }},
    'sound_mode': { mergeWith: 'voiceover_text', fn: (m, t) => {
      if (m && t) {
        let vo = t.trim();
        if (!vo.startsWith('"') && !vo.startsWith('\u201c')) vo = `"${vo}"`;
        return `${m}: ${vo}`;
      }
      return m || t;
    }}
  };
  const skipFields = new Set();
  for (const [, rule] of Object.entries(mergeRules)) {
    if (rule.mergeWith) skipFields.add(rule.mergeWith);
  }
  skipFields.add('custom_location'); // absorbed by setting merge

  // Build values
  const allValues = [];
  for (const { section, fields: sectionFields } of sectionOrder) {
    for (const field of sectionFields) {
      if (mediaAbsorbed.has(field)) {
        if (field === 'media_type' && mediaTypeMerged) {
          allValues.push({ text: mediaTypeMerged, section, field });
        }
        continue;
      }
      if (skipFields.has(field)) continue;
      if (mergeRules[field]) {
        const partner = mergeRules[field].mergeWith;
        const v1 = fields[field], v2 = fields[partner];
        if (v1 || v2) {
          allValues.push({ text: mergeRules[field].fn(v1, v2), section, field });
        }
        continue;
      }
      if (fields[field]) {
        const val = fields[field];
        if (field === 'dialogue') {
          let lines = val;
          if (!lines.startsWith('"') && !lines.startsWith('\u201c')) lines = `"${lines}"`;
          allValues.push({ text: `Dialogue: ${lines}`, section, field });
        } else if (Array.isArray(val)) {
          allValues.push({ text: nlJoin(val), section, field });
        } else {
          allValues.push({ text: val, section, field });
        }
      }
    }
  }

  if (allValues.length === 0) return '';

  // Assemble — subject fields comma-join, gear fields comma-join, others period-join
  const gearFields = new Set(['camera_body', 'focal_length', 'lens_filter']);
  const segments = [];
  let subjectBuf = [], gearBuf = [];
  const flushSubject = () => { if (subjectBuf.length) { segments.push(subjectBuf.map((s, i) => i === 0 ? s.text : (s.field === 'framing' ? '; ' + s.text : ', ' + s.text)).join('')); subjectBuf = []; } };
  const flushGear = () => { if (gearBuf.length) { segments.push(gearBuf.map(g => g.text).join(', ')); gearBuf = []; } };

  for (const v of allValues) {
    if (v.section === 'SUBJECT') { flushGear(); subjectBuf.push(v); }
    else if (v.section === 'CINEMATOGRAPHY' && gearFields.has(v.field)) { flushSubject(); gearBuf.push(v); }
    else { flushSubject(); flushGear(); segments.push(v.text); }
  }
  flushSubject(); flushGear();

  return segments.map(s => {
    let t = s.charAt(0).toUpperCase() + s.slice(1);
    if (!t.endsWith('.') && !t.endsWith('!') && !t.endsWith('"')) t += '.';
    return t;
  }).join(' ');
}

main().catch(err => { console.error(err.message); process.exit(1); });
