const fs = require('fs')
const path = require('path')
const hospitals = require('../data/hospitals.json')
const { getBookingGuide } = require('../core/service')

const OUT_DIR = path.join(__dirname, '..', 'docs', 'clinics')

// Supported languages: pass --lang=en or --lang=zh,en,ja,th to generate multiple
const ALL_LANGS = ['zh', 'en', 'ja', 'th']
const langArg = process.argv.find(a => a.startsWith('--lang='))
const LANGS = langArg
  ? langArg.replace('--lang=', '').split(',').map(l => l.trim()).filter(Boolean)
  : ['zh']

function toSlug(hospital) {
  const id = String(hospital.id).padStart(4, '0')
  const name = (hospital.en_name || hospital.name || String(hospital.id))
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
  return `${id}-${name}`
}

async function main() {
  if (!LANGS.every(l => ALL_LANGS.includes(l))) {
    const invalid = LANGS.filter(l => !ALL_LANGS.includes(l))
    console.error(`❌ Unsupported language(s): ${invalid.join(', ')}. Supported: ${ALL_LANGS.join(', ')}`)
    process.exit(1)
  }

  console.log(`Generating for language(s): ${LANGS.join(', ')}`)

  for (const lang of LANGS) {
    const langDir = LANGS.length > 1 ? path.join(OUT_DIR, lang) : OUT_DIR
    fs.mkdirSync(langDir, { recursive: true })

    let ok = 0
    let fail = 0

    for (const hospital of hospitals) {
      const slug = toSlug(hospital)
      const outPath = path.join(langDir, `${slug}.md`)
      try {
        const content = await getBookingGuide(hospital.name, lang)
        const title = hospital.en_name || hospital.name || slug
        const frontmatter = `---\nlayout: default\ntitle: "${title.replace(/"/g, '\\"')}"\nlang: ${lang}\n---\n\n`
        fs.writeFileSync(outPath, `${frontmatter}${content}\n`, 'utf-8')
        console.log(`✅ [${lang}] ${slug}.md`)
        ok++
      } catch (err) {
        console.error(`❌ [${lang}] ${slug}: ${err.message}`)
        fail++
      }
    }

    console.log(`[${lang}] Done: ${ok} generated, ${fail} failed\n`)
  }
}

main()
