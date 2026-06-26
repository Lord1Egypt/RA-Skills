#!/usr/bin/env node
/**
 * bestseller-writer — Autonomous Book Generator
 * 
 * Usage:
 *   node generate.js --idea "A detective discovers her own murder" --genre thriller
 *   node generate.js --idea "How I built 3 SaaS in 1 year" --genre nonfiction
 *
 * Requires: ANTHROPIC_API_KEY in env
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ─── Config ──────────────────────────────────────────────────────────────────

const args = parseArgs(process.argv.slice(2));
const IDEA = args.idea || args.i;
const GENRE = (args.genre || args.g || 'thriller').toLowerCase();
const OUTPUT_DIR = args.output || args.o || path.join(process.cwd(), 'book-output', slugify(IDEA || 'untitled'));
const MODEL_PLANNER = args.planner || 'claude-opus-4-5';
const MODEL_WRITER = args.writer || 'claude-sonnet-4-5';
const CHAPTERS = parseInt(args.chapters || '25');
const BATCH_SIZE = parseInt(args.batch || '4');

if (!IDEA) {
  console.error('❌ Missing --idea "your book concept here"');
  console.error('');
  console.error('Example:');
  console.error('  node generate.js --idea "A detective discovers her own murder" --genre thriller');
  process.exit(1);
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  console.log(`\n📚 BESTSELLER WRITER`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`💡 Idea: ${IDEA}`);
  console.log(`📖 Genre: ${GENRE}`);
  console.log(`📁 Output: ${OUTPUT_DIR}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const Anthropic = loadAnthropic();
  const client = new Anthropic();

  // ─── Stage 1: Planner ────────────────────────────────────────────────────
  console.log('🧠 [1/5] Running Planner...');
  const plan = await runAgent(client, MODEL_PLANNER, buildPlannerPrompt(IDEA, GENRE, CHAPTERS));
  save(OUTPUT_DIR, 'plan.md', plan);
  console.log(`   ✅ Plan created (${wordCount(plan)} words)\n`);

  // ─── Stage 2: Characters ─────────────────────────────────────────────────
  console.log('👥 [2/5] Building Characters...');
  const isFiction = !['nonfiction', 'non-fiction', 'business', 'self-help', 'memoir'].includes(GENRE);
  const characters = await runAgent(client, MODEL_WRITER, buildCharacterPrompt(plan, GENRE, isFiction));
  save(OUTPUT_DIR, 'characters.md', characters);
  console.log(`   ✅ Characters created\n`);

  // ─── Stage 3: Chapter Writing ─────────────────────────────────────────────
  console.log(`✍️  [3/5] Writing ${CHAPTERS} chapters in parallel batches of ${BATCH_SIZE}...`);
  const chapterOutlines = extractChapterOutlines(plan, CHAPTERS);
  
  for (let batch = 0; batch < CHAPTERS; batch += BATCH_SIZE) {
    const batchNums = Array.from({ length: Math.min(BATCH_SIZE, CHAPTERS - batch) }, (_, i) => batch + i + 1);
    console.log(`   📝 Writing chapters ${batchNums[0]}-${batchNums[batchNums.length - 1]}...`);
    
    const results = await Promise.all(batchNums.map(async (chNum) => {
      const prevChapterPath = path.join(OUTPUT_DIR, `chapter_${String(chNum - 1).padStart(2, '0')}.md`);
      const prevChapter = fs.existsSync(prevChapterPath) ? fs.readFileSync(prevChapterPath, 'utf8').slice(-1500) : '';
      const outline = chapterOutlines[chNum - 1] || `Chapter ${chNum}`;
      const content = await runAgent(client, MODEL_WRITER, buildChapterPrompt(plan, characters, chNum, CHAPTERS, outline, prevChapter, GENRE));
      return { chNum, content };
    }));

    results.forEach(({ chNum, content }) => {
      save(OUTPUT_DIR, `chapter_${String(chNum).padStart(2, '0')}.md`, content);
      console.log(`   ✅ Chapter ${chNum} (${wordCount(content)} words)`);
    });
  }

  console.log('');

  // ─── Stage 4: Editor ─────────────────────────────────────────────────────
  console.log('🔍 [4/5] Running Editor...');
  const allChapters = readAllChapters(OUTPUT_DIR, CHAPTERS);
  const editorial = await runAgent(client, MODEL_PLANNER, buildEditorPrompt(plan, allChapters, GENRE));
  save(OUTPUT_DIR, 'editorial_memo.md', editorial);
  console.log(`   ✅ Editorial pass complete\n`);

  // ─── Stage 5: KDP Packager ────────────────────────────────────────────────
  console.log('📦 [5/5] Creating KDP Package...');
  const kdpPackage = await runAgent(client, MODEL_WRITER, buildKDPPrompt(plan, editorial, GENRE));
  save(OUTPUT_DIR, 'kdp_package.md', kdpPackage);
  console.log(`   ✅ KDP package ready\n`);

  // ─── Assemble Final Manuscript ────────────────────────────────────────────
  console.log('📎 Assembling final manuscript...');
  const manuscript = assembleManuscript(OUTPUT_DIR, CHAPTERS, plan);
  save(OUTPUT_DIR, 'MANUSCRIPT.md', manuscript);
  
  const totalWords = wordCount(manuscript);
  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`✅ BOOK COMPLETE`);
  console.log(`📊 Total words: ${totalWords.toLocaleString()}`);
  console.log(`📁 Output: ${OUTPUT_DIR}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`\nFiles:`);
  console.log(`  📄 MANUSCRIPT.md      — Full book`);
  console.log(`  📦 kdp_package.md     — Amazon publishing package`);
  console.log(`  🗒️  plan.md            — Story structure`);
  console.log(`  👥 characters.md      — Character profiles`);
  console.log(`  📝 editorial_memo.md  — Editor notes\n`);
}

// ─── Prompts ──────────────────────────────────────────────────────────────────

function buildPlannerPrompt(idea, genre, chapters) {
  const isNonFiction = ['nonfiction', 'non-fiction', 'business', 'self-help', 'memoir'].includes(genre);
  return `You are a New York Times bestselling book strategist and developmental editor.

The user has this book idea: "${idea}"
Genre: ${genre}
Target chapters: ${chapters}

Your job is to create a comprehensive, commercially viable book plan.

## Output Format

### 1. MARKET POSITIONING
- Genre and sub-genre (be specific)
- Target reader (demographics + psychographics, NOT just "fans of X genre")
- The ONE sentence pitch (elevator pitch)
- 3 comparable titles published in the last 3 years (be realistic and accurate)
- Why this book will sell NOW (market timing)

### 2. TITLE OPTIONS (5 options, ranked)
Format: **[Title]: [Subtitle]**
Optimize for: searchability + emotional hook + memorability

### 3. BOOK OVERVIEW
- Core premise (2-3 paragraphs)
- Central conflict or central question the book answers
- Emotional journey for the reader
- The "only book you'll ever need on X" claim

### 4. STRUCTURE
${isNonFiction ? `
- Core framework (give it a NAME — acronym or metaphor)
- Key transformation: reader goes from [STATE A] to [STATE B]
- Major sections (3-5 parts)
` : `
- 3-act structure breakdown
- Major turning points (inciting incident, midpoint, all-is-lost, climax)
- Themes
`}

### 5. CHAPTER OUTLINE (${chapters} chapters)
For EACH chapter:
**Chapter [N]: [Title]**
- [1-2 sentence description of what happens/is revealed]
- Hook: [How this chapter ends to make reader turn page]

${isNonFiction ? `
### 6. KEY INSIGHTS/ARGUMENTS
List the 10 most compelling ideas/insights in the book that will generate word-of-mouth.
` : `
### 6. PLOT THREADS
List the 3-4 major plot threads and how they intersect.
`}

Write the complete plan now. Be specific, commercially savvy, and make this book impossible to put down.`;
}

function buildCharacterPrompt(plan, genre, isFiction) {
  if (!isFiction) {
    return `You are creating the authority framework for a ${genre} book.

Here is the book plan:
${plan.slice(0, 3000)}

Create:

## AUTHOR AUTHORITY PERSONA
- What makes YOU the right person to write this book
- Your unique methodology (give it a memorable name)
- Your core transformation promise
- 3 myths/misconceptions you'll debunk
- Your "against the grain" contrarian take that makes this book different

## IDEAL READER AVATAR
- Name them (e.g., "Struggling Steve" or "Ambitious Anna")
- Age, occupation, income level
- Top 3 burning problems
- What they've tried before (and why it failed)
- Their dream outcome in vivid detail
- Where they hang out (subreddits, podcasts, YouTube channels)
- The exact words they use to describe their problem

## CORE FRAMEWORK
- Framework name and acronym
- Each component explained (1 paragraph each)
- Visual/diagram description
- The "aha moment" each chapter should produce

Be specific and commercially sharp.`;
  }

  return `You are a character development specialist. Create rich, publishable character profiles.

Here is the book plan:
${plan.slice(0, 3000)}

## PROTAGONIST
- Full name + nickname
- Age, appearance (specific, memorable details — not generic)
- Occupation and world
- **Core Wound**: What broke them in the past (must be specific trauma/event)
- **Want**: What they think they need (surface desire)
- **Need**: What they actually need (deeper truth, usually opposite of Want)
- **Lie They Believe**: The false belief driving bad decisions
- **Ghost**: The past event that haunts them
- **Fatal Flaw**: What will destroy them if not overcome
- **Strength**: What makes them capable of winning
- **Arc**: Where they START vs. END emotionally (be specific)
- **Voice Sample**: 3 lines of dialogue that capture how they speak

## ANTAGONIST (if applicable)
Same format as protagonist.
Critical: The antagonist must believe they are the hero of their own story. Give them a compelling reason for what they do.

## SUPPORTING CAST (3-5 characters)
For each:
- Name + role
- Relationship to protagonist
- Their function in the story (mirror, mentor, shapeshifter, etc.)
- One distinctive trait readers will remember
- Their arc (even minor characters should change)

## RELATIONSHIP MAP
Describe how each character connects and creates conflict/tension.

## VOICE GUIDE
For each major character, give:
- Speech pattern (formal/casual/clipped/verbose)
- Vocabulary level
- What they talk about too much
- What they never say
- Sample: 3 lines of unique dialogue`;
}

function buildChapterPrompt(plan, characters, chNum, totalChapters, outline, prevChapter, genre) {
  const isNonFiction = ['nonfiction', 'non-fiction', 'business', 'self-help', 'memoir'].includes(genre);
  const isFinal = chNum === totalChapters;
  const isFirst = chNum === 1;

  return `You are writing Chapter ${chNum} of ${totalChapters} of a ${genre} book.

## BOOK CONTEXT (PLAN SUMMARY)
${plan.slice(0, 2000)}

## CHARACTER PROFILES
${characters.slice(0, 1500)}

## THIS CHAPTER
${outline}

${prevChapter ? `## PREVIOUS CHAPTER ENDING
${prevChapter}
` : ''}

## WRITING INSTRUCTIONS

Write Chapter ${chNum} now. Follow these rules:

**LENGTH**: 2,000-2,500 words (never shorter than 1,800)

**OPENING**: 
${isFirst ? '- First sentence must hook immediately. No setup. Start in the middle of action or tension.' : '- Pick up the thread from the previous chapter. Create continuity.'}

**CRAFT RULES**:
- Vary sentence length. Tension = short. Emotion = long.
- Every scene must do TWO things simultaneously (advance plot AND reveal character)
- No adverbs unless absolutely necessary ("he whispered" not "he said quietly")
- Dialogue feels real: people interrupt, trail off, don't explain themselves to each other
- Show don't tell: never write "she felt sad" — show behavior that signals emotion
- Every paragraph should end with a reason to read the next one

${isNonFiction ? `
**NON-FICTION STRUCTURE**:
- Open with a story or provocative question/stat
- Introduce the concept clearly with a simple definition
- Give 2 concrete real-world examples (can be composite/illustrative)
- Explain the "so what" — why this matters to the reader
- End with a specific action item or reflection question
` : `
**FICTION CRAFT**:
- Stay in consistent POV
- Ground every scene with sensory details (what do they see, hear, smell?)
- Use subtext in dialogue — characters say one thing, mean another
- Plant a seed for a later payoff if this is early in the book
`}

**CHAPTER ENDING**:
${isFinal ? '- Deliver the emotional payoff the book has been building toward. Satisfying but not sappy.' : '- End with a hook that FORCES the reader to turn the page. Question, revelation, threat, or cliffhanger.'}

Write the complete chapter now. No preamble. Start writing.`;
}

function buildEditorPrompt(plan, allChapters, genre) {
  const sampleChapters = allChapters.slice(0, 8000); // first ~3 chapters for review
  return `You are a senior developmental editor at Penguin Random House with 20 years experience.

## BOOK PLAN
${plan.slice(0, 1500)}

## MANUSCRIPT SAMPLE (First chapters)
${sampleChapters}

## YOUR JOB

### 1. OVERALL VERDICT
Is this publishable? What's the strongest aspect? What's the biggest weakness?

### 2. PACING ANALYSIS
- Does the story/argument move at the right speed?
- Which chapters drag? (list by number)
- Which chapters rush? (list by number)
- Recommendation for each

### 3. VOICE CONSISTENCY
- Is the voice consistent throughout?
- Where does it break?
- How to fix it?

### 4. OPENING ASSESSMENT
- Is Chapter 1 strong enough to hook an agent in 3 pages?
- If not: specific rewrite suggestions

### 5. STRUCTURAL ISSUES
- Any plot holes or logical gaps?
- Does the ending deliver on the book's promise?
- What's missing?

### 6. LINE-LEVEL NOTES
- 5 specific examples of strong writing (quote + why it works)
- 5 specific examples of weak writing (quote + how to fix)

### 7. MARKETABILITY SCORE
Rate 1-10 and explain:
- Commercial appeal
- Originality
- Execution quality
- Competition in market

### 8. FINAL TITLE RECOMMENDATION
Based on what you've read, pick the best title and explain why.

Be direct. This author needs honest feedback, not validation.`;
}

function buildKDPPrompt(plan, editorial, genre) {
  return `You are an Amazon KDP publishing specialist who has launched 200+ books.

## BOOK PLAN
${plan.slice(0, 2000)}

## EDITORIAL ASSESSMENT
${editorial.slice(0, 1000)}

Create the complete Amazon KDP publishing package:

---

## TITLE OPTIONS (5, ranked best to worst)
Format: **[Title]: [Subtitle]**
Rules: Title ≤6 words, subtitle front-loads keyword, together ≤12 words

## CHOSEN TITLE
**[Best Option]**
Reason: [1 sentence why]

## AMAZON DESCRIPTION (150-200 words)
- **First sentence in bold** (the hook — make it emotional and specific)
- Paragraph 2: Setup + conflict
- Paragraph 3: Stakes + promise
- Paragraph 4: Social proof framing ("Readers who loved X will devour this")
- Final line: CTA ("Get your copy now" or "Start reading today")
- Naturally weave in 3-4 keywords readers actually search

## 7 KEYWORD STRINGS
(Each ≤50 characters, these go in KDP's 7 keyword fields)
Target buyer-intent keywords, not genre names
Example: "page turning thriller with twist ending" not just "thriller"

1. 
2.
3.
4.
5.
6.
7.

## BISAC CATEGORIES
- Primary: [exact BISAC code + name]
- Secondary: [exact BISAC code + name]

## PRICING STRATEGY
- Launch price: $X.XX (and why)
- Post-launch price: $X.XX
- KDP Select? Yes/No (and why)
- Free promo timing recommendation

## AUTHOR BIO (150 words, third person)
Authority-forward. Relatable ending. Include expertise signals.

## BACK COVER COPY (100 words)
Hook → Promise → Proof → CTA

## COVER DESIGN BRIEF
- Style: [photographic/illustrated/minimalist/typographic]
- Mood: [3 adjectives]
- Color palette: [3 hex codes or descriptors]
- Key visual element
- Font style (serif/sans-serif + energy)
- 3 comparable book covers to reference
- Midjourney prompt: [full usable prompt]

## LAUNCH CHECKLIST
- [ ] Upload manuscript (EPUB or DOCX)
- [ ] Upload cover (2560x1600px minimum)
- [ ] Set pricing and territories
- [ ] Enroll in KDP Select (recommended for launch)
- [ ] Schedule free promo for day 5-9 post-launch
- [ ] Set up Author Central page
- [ ] Prepare 10 review outreach emails`;
}

// ─── Agent Runner ─────────────────────────────────────────────────────────────

async function runAgent(client, model, prompt) {
  const response = await client.messages.create({
    model,
    max_tokens: 8192,
    messages: [{ role: 'user', content: prompt }]
  });
  return response.content[0].text;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function extractChapterOutlines(plan, totalChapters) {
  const outlines = [];
  const lines = plan.split('\n');
  for (const line of lines) {
    const match = line.match(/chapter\s+(\d+)[:\s]+(.+)/i);
    if (match) {
      const num = parseInt(match[1]);
      if (num >= 1 && num <= totalChapters) {
        outlines[num - 1] = match[2].trim();
      }
    }
  }
  // Fill gaps
  for (let i = 0; i < totalChapters; i++) {
    if (!outlines[i]) outlines[i] = `Chapter ${i + 1}`;
  }
  return outlines;
}

function readAllChapters(dir, total) {
  const parts = [];
  for (let i = 1; i <= total; i++) {
    const p = path.join(dir, `chapter_${String(i).padStart(2, '0')}.md`);
    if (fs.existsSync(p)) parts.push(fs.readFileSync(p, 'utf8'));
  }
  return parts.join('\n\n---\n\n');
}

function assembleManuscript(dir, total, plan) {
  const titleMatch = plan.match(/\*\*([^*]+?)\*\*.*?subtitle/i) || plan.match(/Title[:\s]+\*\*([^*]+)\*\*/i);
  const title = titleMatch ? titleMatch[1] : 'Untitled';
  
  let manuscript = `# ${title}\n\n---\n\n`;
  for (let i = 1; i <= total; i++) {
    const p = path.join(dir, `chapter_${String(i).padStart(2, '0')}.md`);
    if (fs.existsSync(p)) {
      manuscript += fs.readFileSync(p, 'utf8');
      manuscript += '\n\n---\n\n';
    }
  }
  return manuscript;
}

function save(dir, filename, content) {
  fs.writeFileSync(path.join(dir, filename), content, 'utf8');
}

function wordCount(text) {
  return text.split(/\s+/).filter(Boolean).length;
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40);
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      result[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    } else if (argv[i].startsWith('-') && argv[i].length === 2) {
      const key = argv[i].slice(1);
      result[key] = argv[i + 1] && !argv[i + 1].startsWith('-') ? argv[++i] : true;
    }
  }
  return result;
}

function loadAnthropic() {
  try {
    return require('@anthropic-ai/sdk');
  } catch {
    console.error('❌ Missing dependency: @anthropic-ai/sdk');
    console.error('   Run: npm install @anthropic-ai/sdk');
    process.exit(1);
  }
}

// ─── Run ─────────────────────────────────────────────────────────────────────

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  process.exit(1);
});
