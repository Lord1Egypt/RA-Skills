/**
 * benchmark-recall-en.ts — Vector-free recall benchmark (English)
 * Usage: npx tsx cc-soul/benchmark-recall-en.ts
 */

import { createRequire } from 'module'
import type { Memory } from './types.ts'

const require = createRequire(import.meta.url)
;(globalThis as any).require = require
process.env.CC_SOUL_BENCHMARK = "1"

// Lazy-load modules to avoid side effects
const { activationRecall } = require('./activation-field.ts')
const { expandQuery, learnAssociation } = require('./aam.ts')

// ═══════════════════════════════════════════════════════════════
// TEST DATA: 200 English memories
// ═══════════════════════════════════════════════════════════════

const DAY = 86400000

const TEST_MEMORIES: Memory[] = [
  // ── Original 40 (index 0–39) ──────────────────────────────────
  /* 0  */ { content: 'I wake up at 6am every day', scope: 'fact', ts: Date.now() - DAY * 30, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - DAY * 2 },
  /* 1  */ { content: "I'm allergic to shellfish", scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.92, recallCount: 4, lastAccessed: Date.now() - DAY * 15 },
  /* 2  */ { content: 'My car is a BMW 3 Series, 2022 model', scope: 'fact', ts: Date.now() - DAY * 90, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - DAY * 10 },
  /* 3  */ { content: 'I got promoted to senior engineer last month', scope: 'fact', ts: Date.now() - DAY * 25, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 4  */ { content: 'My son plays soccer every Saturday', scope: 'fact', ts: Date.now() - DAY * 60, confidence: 0.85, recallCount: 5, lastAccessed: Date.now() - DAY * 7 },
  /* 5  */ { content: 'I quit drinking 3 months ago', scope: 'fact', ts: Date.now() - DAY * 15, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 6  */ { content: "I'm afraid of heights", scope: 'fact', ts: Date.now() - DAY * 150, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },
  /* 7  */ { content: 'Planning a trip to Italy in June', scope: 'episode', ts: Date.now() - DAY * 5, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 8  */ { content: 'My college roommate Kevin works at Google now', scope: 'fact', ts: Date.now() - DAY * 120, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - DAY * 20 },
  /* 9  */ { content: 'My blood type is A positive', scope: 'fact', ts: Date.now() - DAY * 250, confidence: 0.95, recallCount: 1, lastAccessed: Date.now() - DAY * 60 },
  /* 10 */ { content: 'I usually read before bed', scope: 'fact', ts: Date.now() - DAY * 45, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 11 */ { content: "I'm thinking about doing an MBA", scope: 'fact', ts: Date.now() - DAY * 10, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - DAY * 2 },
  /* 12 */ { content: 'Lost $5000 in crypto last year', scope: 'fact', ts: Date.now() - DAY * 180, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 25 },
  /* 13 */ { content: "I'm learning Spanish, about A2 level", scope: 'fact', ts: Date.now() - DAY * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 14 */ { content: 'Met my wife on a dating app', scope: 'fact', ts: Date.now() - DAY * 300, confidence: 0.93, recallCount: 5, lastAccessed: Date.now() - DAY * 40 },
  /* 15 */ { content: 'I use a ThinkPad X1 Carbon for work', scope: 'fact', ts: Date.now() - DAY * 50, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 8 },
  /* 16 */ { content: 'I play basketball every Wednesday', scope: 'fact', ts: Date.now() - DAY * 35, confidence: 0.83, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 17 */ { content: 'Currently reading Sapiens by Yuval Harari', scope: 'fact', ts: Date.now() - DAY * 8, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 2 },
  /* 18 */ { content: 'Had knee surgery two years ago', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - DAY * 35 },
  /* 19 */ { content: 'I work at Microsoft as a PM', scope: 'fact', ts: Date.now() - DAY * 20, confidence: 0.92, recallCount: 6, lastAccessed: Date.now() - DAY * 1 },
  /* 20 */ { content: "My daughter's birthday is March 15", scope: 'fact', ts: Date.now() - DAY * 70, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 10 },
  /* 21 */ { content: 'I prefer Python over Java', scope: 'preference', ts: Date.now() - DAY * 110, confidence: 0.87, recallCount: 4, lastAccessed: Date.now() - DAY * 12 },
  /* 22 */ { content: 'My mortgage is $2500/month', scope: 'fact', ts: Date.now() - DAY * 55, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 23 */ { content: 'I meditate for 20 minutes every morning', scope: 'fact', ts: Date.now() - DAY * 28, confidence: 0.88, recallCount: 5, lastAccessed: Date.now() - DAY * 1 },
  /* 24 */ { content: 'My mom lives in Chicago', scope: 'fact', ts: Date.now() - DAY * 365, confidence: 0.95, recallCount: 4, lastAccessed: Date.now() - DAY * 20 },
  /* 25 */ { content: "I'm training for a half marathon", scope: 'fact', ts: Date.now() - DAY * 12, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 26 */ { content: 'I switched from iPhone to Android last year', scope: 'fact', ts: Date.now() - DAY * 160, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },
  /* 27 */ { content: 'I have two cats named Luna and Mochi', scope: 'fact', ts: Date.now() - DAY * 80, confidence: 0.9, recallCount: 6, lastAccessed: Date.now() - DAY * 1 },
  /* 28 */ { content: "My favorite restaurant is the Italian place on 5th Street", scope: 'preference', ts: Date.now() - DAY * 130, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 7 },
  /* 29 */ { content: "I've been having back pain since January", scope: 'fact', ts: Date.now() - DAY * 18, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 4 },
  /* 30 */ { content: 'I volunteer at the food bank on Sundays', scope: 'fact', ts: Date.now() - DAY * 42, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 31 */ { content: 'My team has 8 people', scope: 'fact', ts: Date.now() - DAY * 22, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 32 */ { content: 'I commute by train, takes 45 minutes', scope: 'fact', ts: Date.now() - DAY * 65, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 1 },
  /* 33 */ { content: "I'm considering buying a house", scope: 'fact', ts: Date.now() - DAY * 3, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 34 */ { content: 'My best friend Dave lives in London', scope: 'fact', ts: Date.now() - DAY * 140, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 18 },
  /* 35 */ { content: 'I do intermittent fasting, 16:8', scope: 'fact', ts: Date.now() - DAY * 38, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 36 */ { content: 'Last vacation was in Bali, loved it', scope: 'episode', ts: Date.now() - DAY * 170, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 40 },
  /* 37 */ { content: "I'm mentoring two junior engineers", scope: 'fact', ts: Date.now() - DAY * 14, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 3 },
  /* 38 */ { content: 'My annual review is in December', scope: 'fact', ts: Date.now() - DAY * 48, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 39 */ { content: 'I started a side project, a recipe app', scope: 'fact', ts: Date.now() - DAY * 7, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },

  // ── Index 40–79 ──────────────────────────────────────────────
  /* 40 */ { content: 'I drink oat milk instead of regular milk', scope: 'preference', ts: Date.now() - DAY * 75, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 4 },
  /* 41 */ { content: 'My favorite TV show is Breaking Bad', scope: 'preference', ts: Date.now() - DAY * 200, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - DAY * 30 },
  /* 42 */ { content: 'I wake up at 5:30am on weekdays for the gym', scope: 'fact', ts: Date.now() - DAY * 20, confidence: 0.88, recallCount: 5, lastAccessed: Date.now() - DAY * 1 },
  /* 43 */ { content: "I'm vegetarian, have been for 3 years", scope: 'fact', ts: Date.now() - DAY * 180, confidence: 0.92, recallCount: 4, lastAccessed: Date.now() - DAY * 6 },
  /* 44 */ { content: 'My sister lives in Seattle, we FaceTime every Sunday', scope: 'fact', ts: Date.now() - DAY * 150, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - DAY * 3 },
  /* 45 */ { content: "I've been journaling every night before bed", scope: 'fact', ts: Date.now() - DAY * 35, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 1 },
  /* 46 */ { content: 'My car insurance is with Geico, about $150/month', scope: 'fact', ts: Date.now() - DAY * 90, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 47 */ { content: "I'm learning to play guitar, bought one last month", scope: 'fact', ts: Date.now() - DAY * 8, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 2 },
  /* 48 */ { content: 'I use Notion for all my note-taking', scope: 'fact', ts: Date.now() - DAY * 60, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 49 */ { content: 'My childhood dream was to be an astronaut', scope: 'fact', ts: Date.now() - DAY * 300, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 50 },
  /* 50 */ { content: 'I hate spiders, had a bad experience as a kid', scope: 'fact', ts: Date.now() - DAY * 220, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 25 },
  /* 51 */ { content: 'I donate to the Red Cross every Christmas', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 60 },
  /* 52 */ { content: 'My favorite cuisine is Thai food', scope: 'preference', ts: Date.now() - DAY * 110, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - DAY * 8 },
  /* 53 */ { content: 'I have a standing desk at home', scope: 'fact', ts: Date.now() - DAY * 45, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 54 */ { content: "I'm trying to reduce my screen time to under 3 hours", scope: 'fact', ts: Date.now() - DAY * 15, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 3 },
  /* 55 */ { content: 'I broke my arm playing football in college', scope: 'fact', ts: Date.now() - DAY * 280, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 45 },
  /* 56 */ { content: "My neighbor's dog barks every morning at 6am", scope: 'fact', ts: Date.now() - DAY * 30, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 57 */ { content: 'I subscribe to Netflix, Disney+, and HBO Max', scope: 'fact', ts: Date.now() - DAY * 55, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 4 },
  /* 58 */ { content: "I'm planning to propose to my girlfriend in September", scope: 'fact', ts: Date.now() - DAY * 5, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 59 */ { content: 'My grandma taught me how to make pasta from scratch', scope: 'fact', ts: Date.now() - DAY * 350, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 35 },
  /* 60 */ { content: 'I run 5K every Tuesday and Thursday morning', scope: 'fact', ts: Date.now() - DAY * 25, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 2 },
  /* 61 */ { content: "My brother is a dentist in Portland", scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 22 },
  /* 62 */ { content: 'I have a peanut allergy, carry an EpiPen', scope: 'fact', ts: Date.now() - DAY * 250, confidence: 0.95, recallCount: 4, lastAccessed: Date.now() - DAY * 10 },
  /* 63 */ { content: 'My favorite band is Radiohead', scope: 'preference', ts: Date.now() - DAY * 180, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - DAY * 15 },
  /* 64 */ { content: 'I take vitamin D and omega-3 supplements daily', scope: 'fact', ts: Date.now() - DAY * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 3 },
  /* 65 */ { content: "I'm saving up for a Tesla Model 3", scope: 'fact', ts: Date.now() - DAY * 10, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 2 },
  /* 66 */ { content: 'I coached my daughter\'s soccer team last season', scope: 'fact', ts: Date.now() - DAY * 120, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 28 },
  /* 67 */ { content: 'I have a tattoo of a compass on my left forearm', scope: 'fact', ts: Date.now() - DAY * 400, confidence: 0.92, recallCount: 2, lastAccessed: Date.now() - DAY * 55 },
  /* 68 */ { content: 'I failed my first driving test when I was 16', scope: 'fact', ts: Date.now() - DAY * 350, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - DAY * 70 },
  /* 69 */ { content: 'My WiFi password is taped under the router', scope: 'fact', ts: Date.now() - DAY * 80, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 12 },
  /* 70 */ { content: 'I always order extra hot sauce on my burrito', scope: 'preference', ts: Date.now() - DAY * 95, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 6 },
  /* 71 */ { content: 'I did a coding bootcamp before my CS degree', scope: 'fact', ts: Date.now() - DAY * 320, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 40 },
  /* 72 */ { content: "I'm on a waitlist for a golden retriever puppy", scope: 'fact', ts: Date.now() - DAY * 6, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 73 */ { content: 'I sleep with a white noise machine', scope: 'fact', ts: Date.now() - DAY * 70, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 4 },
  /* 74 */ { content: 'I got food poisoning from sushi last month', scope: 'episode', ts: Date.now() - DAY * 4, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 75 */ { content: 'My favorite movie is The Shawshank Redemption', scope: 'preference', ts: Date.now() - DAY * 190, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 20 },
  /* 76 */ { content: 'I maxed out my 401k contributions this year', scope: 'fact', ts: Date.now() - DAY * 12, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - DAY * 5 },
  /* 77 */ { content: 'I have a fear of public speaking', scope: 'fact', ts: Date.now() - DAY * 160, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - DAY * 18 },
  /* 78 */ { content: 'I built a treehouse for my kids last summer', scope: 'episode', ts: Date.now() - DAY * 240, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 50 },
  /* 79 */ { content: 'My go-to coffee order is a flat white with oat milk', scope: 'preference', ts: Date.now() - DAY * 50, confidence: 0.86, recallCount: 5, lastAccessed: Date.now() - DAY * 1 },

  // ── New 120 (index 80–199) ──────────────────────────────────
  // Work details
  /* 80  */ { content: 'Our main project at work is called Project Aurora, a cloud migration tool', scope: 'fact', ts: Date.now() - DAY * 18, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - DAY * 2 },
  /* 81  */ { content: 'My tech stack at work is React, TypeScript, and Azure', scope: 'fact', ts: Date.now() - DAY * 30, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - DAY * 1 },
  /* 82  */ { content: 'My coworker Sarah always brings donuts on Fridays', scope: 'fact', ts: Date.now() - DAY * 45, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 83  */ { content: 'I got a "exceeds expectations" on my last performance review', scope: 'fact', ts: Date.now() - DAY * 60, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 84  */ { content: 'Our team uses Jira for project management', scope: 'fact', ts: Date.now() - DAY * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 3 },
  /* 85  */ { content: 'My manager is named Tom, he joined from Amazon', scope: 'fact', ts: Date.now() - DAY * 90, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },
  /* 86  */ { content: 'I presented at the company all-hands meeting last quarter', scope: 'episode', ts: Date.now() - DAY * 55, confidence: 0.84, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 87  */ { content: 'We have a team offsite in Austin next month', scope: 'episode', ts: Date.now() - DAY * 3, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 88  */ { content: 'I have 18 days of PTO remaining this year', scope: 'fact', ts: Date.now() - DAY * 10, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 3 },
  /* 89  */ { content: 'My work laptop has 32GB RAM and an i7 processor', scope: 'fact', ts: Date.now() - DAY * 50, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 90  */ { content: 'I got a $15k bonus last year for shipping Project Aurora on time', scope: 'fact', ts: Date.now() - DAY * 70, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 91  */ { content: 'We do standups at 9:30am every morning on Teams', scope: 'fact', ts: Date.now() - DAY * 25, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 1 },

  // Family details
  /* 92  */ { content: 'My dad is a retired high school math teacher', scope: 'fact', ts: Date.now() - DAY * 300, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - DAY * 25 },
  /* 93  */ { content: 'My mom worked as a nurse for 30 years before retiring', scope: 'fact', ts: Date.now() - DAY * 310, confidence: 0.93, recallCount: 3, lastAccessed: Date.now() - DAY * 25 },
  /* 94  */ { content: 'My younger sister Emma is getting married in October', scope: 'fact', ts: Date.now() - DAY * 8, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 95  */ { content: 'We have a big family reunion at Thanksgiving every year at my parents place', scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - DAY * 30 },
  /* 96  */ { content: 'My son is in 3rd grade at Lincoln Elementary', scope: 'fact', ts: Date.now() - DAY * 40, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 97  */ { content: 'My wife works as an interior designer, runs her own studio', scope: 'fact', ts: Date.now() - DAY * 150, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 98  */ { content: 'My father-in-law is a retired Army colonel', scope: 'fact', ts: Date.now() - DAY * 250, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 35 },
  /* 99  */ { content: 'My parents celebrated their 40th wedding anniversary last year', scope: 'episode', ts: Date.now() - DAY * 180, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 40 },
  /* 100 */ { content: 'My daughter wants to be a veterinarian when she grows up', scope: 'fact', ts: Date.now() - DAY * 35, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 7 },
  /* 101 */ { content: 'My uncle owns a vineyard in Napa Valley', scope: 'fact', ts: Date.now() - DAY * 280, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 45 },

  // Health details
  /* 102 */ { content: 'I have mild asthma, use an inhaler occasionally', scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 12 },
  /* 103 */ { content: 'I take 10mg of melatonin when I have trouble sleeping', scope: 'fact', ts: Date.now() - DAY * 45, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 8 },
  /* 104 */ { content: 'My doctor recommended I get my cholesterol checked every 6 months', scope: 'fact', ts: Date.now() - DAY * 30, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 105 */ { content: 'I had my wisdom teeth removed when I was 20', scope: 'fact', ts: Date.now() - DAY * 320, confidence: 0.88, recallCount: 1, lastAccessed: Date.now() - DAY * 60 },
  /* 106 */ { content: 'I wear contact lenses, -3.5 prescription in both eyes', scope: 'fact', ts: Date.now() - DAY * 150, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 10 },
  /* 107 */ { content: 'I see a chiropractor every two weeks for my back', scope: 'fact', ts: Date.now() - DAY * 15, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 3 },
  /* 108 */ { content: 'I have a dental cleaning scheduled for next Tuesday', scope: 'episode', ts: Date.now() - DAY * 2, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - DAY * 1 },
  /* 109 */ { content: 'My resting heart rate is around 58 bpm thanks to running', scope: 'fact', ts: Date.now() - DAY * 20, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 5 },
  /* 110 */ { content: 'I had a concussion playing football in high school', scope: 'fact', ts: Date.now() - DAY * 350, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - DAY * 55 },

  // Finance details
  /* 111 */ { content: 'I invest mostly in index funds, about 70% of my portfolio', scope: 'fact', ts: Date.now() - DAY * 60, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },
  /* 112 */ { content: 'My salary is $165k base plus bonus', scope: 'fact', ts: Date.now() - DAY * 25, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 113 */ { content: 'I have term life insurance, $500k coverage through Northwestern Mutual', scope: 'fact', ts: Date.now() - DAY * 120, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 25 },
  /* 114 */ { content: 'I owe about $28k left on my car loan', scope: 'fact', ts: Date.now() - DAY * 50, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 12 },
  /* 115 */ { content: 'I use TurboTax to file my taxes, usually get a $2k refund', scope: 'fact', ts: Date.now() - DAY * 80, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },
  /* 116 */ { content: 'I have a Roth IRA in addition to my 401k', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 117 */ { content: 'My credit score is around 780', scope: 'fact', ts: Date.now() - DAY * 35, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 118 */ { content: 'I have an emergency fund covering 6 months of expenses', scope: 'fact', ts: Date.now() - DAY * 70, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 18 },

  // Social details
  /* 119 */ { content: 'My friend group has a poker night the first Friday of every month', scope: 'fact', ts: Date.now() - DAY * 45, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 5 },
  /* 120 */ { content: 'I threw a surprise birthday party for my wife last year at a rooftop bar', scope: 'episode', ts: Date.now() - DAY * 180, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },
  /* 121 */ { content: 'My college buddy Mike moved back from Japan last month', scope: 'fact', ts: Date.now() - DAY * 6, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 2 },
  /* 122 */ { content: 'I met up with Dave in London when I was there for a conference', scope: 'episode', ts: Date.now() - DAY * 90, confidence: 0.84, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 123 */ { content: 'We have a neighborhood BBQ every 4th of July', scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 35 },
  /* 124 */ { content: "My friend Lisa is a sommelier, she always picks the wine at dinner", scope: 'fact', ts: Date.now() - DAY * 130, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 125 */ { content: 'I hosted a game night last weekend with 12 people', scope: 'episode', ts: Date.now() - DAY * 2, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },
  /* 126 */ { content: 'My friend group from college still has a group chat that is very active', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 4 },

  // Education details
  /* 127 */ { content: 'I graduated from University of Michigan with a CS degree in 2016', scope: 'fact', ts: Date.now() - DAY * 400, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - DAY * 30 },
  /* 128 */ { content: 'My favorite professor was Dr. Chen who taught algorithms', scope: 'fact', ts: Date.now() - DAY * 380, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 50 },
  /* 129 */ { content: 'I almost failed organic chemistry in my freshman year', scope: 'fact', ts: Date.now() - DAY * 390, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 55 },
  /* 130 */ { content: 'I was in the computer science club and we won a hackathon in 2015', scope: 'fact', ts: Date.now() - DAY * 370, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 45 },
  /* 131 */ { content: 'I wrote my senior thesis on distributed systems fault tolerance', scope: 'fact', ts: Date.now() - DAY * 360, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - DAY * 40 },
  /* 132 */ { content: 'I had a scholarship that covered 50% of my tuition', scope: 'fact', ts: Date.now() - DAY * 400, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 50 },
  /* 133 */ { content: 'I studied abroad in Berlin for one semester', scope: 'fact', ts: Date.now() - DAY * 380, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 40 },
  /* 134 */ { content: 'I was a TA for the intro to programming class in my senior year', scope: 'fact', ts: Date.now() - DAY * 370, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 45 },

  // Hobby details
  /* 135 */ { content: 'I completed a 1000-piece puzzle of Starry Night last month', scope: 'episode', ts: Date.now() - DAY * 8, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 3 },
  /* 136 */ { content: 'I brew my own beer at home, an IPA is my best recipe', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 10 },
  /* 137 */ { content: 'I finished a half marathon in 1 hour 52 minutes last fall', scope: 'episode', ts: Date.now() - DAY * 120, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 15 },
  /* 138 */ { content: 'I collect vintage vinyl records, have about 200 in my collection', scope: 'fact', ts: Date.now() - DAY * 160, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },
  /* 139 */ { content: 'I do woodworking on weekends, built a bookshelf last month', scope: 'fact', ts: Date.now() - DAY * 12, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 3 },
  /* 140 */ { content: 'I placed 3rd in a local photography contest with a sunset shot', scope: 'episode', ts: Date.now() - DAY * 75, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 141 */ { content: 'I grow tomatoes, basil, and peppers in my backyard garden', scope: 'fact', ts: Date.now() - DAY * 50, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 142 */ { content: 'I have been playing chess online, my rating is about 1200 on chess.com', scope: 'fact', ts: Date.now() - DAY * 30, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 3 },

  // Daily routine details
  /* 143 */ { content: 'I take the 7:15am express train from Hoboken to Penn Station', scope: 'fact', ts: Date.now() - DAY * 65, confidence: 0.87, recallCount: 4, lastAccessed: Date.now() - DAY * 1 },
  /* 144 */ { content: 'I eat lunch at my desk around 12:30, usually a salad from Sweetgreen', scope: 'fact', ts: Date.now() - DAY * 20, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 145 */ { content: 'I pick up my son from soccer practice at 5pm on Saturdays', scope: 'fact', ts: Date.now() - DAY * 55, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 146 */ { content: 'I brew coffee at home with a Chemex pour-over every morning', scope: 'fact', ts: Date.now() - DAY * 40, confidence: 0.85, recallCount: 5, lastAccessed: Date.now() - DAY * 1 },
  /* 147 */ { content: 'I usually finish work by 6pm and am home by 7pm', scope: 'fact', ts: Date.now() - DAY * 35, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 148 */ { content: 'I walk the cats around the block at 8pm, Luna loves it but Mochi just sits', scope: 'fact', ts: Date.now() - DAY * 25, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - DAY * 2 },
  /* 149 */ { content: 'I listen to podcasts during my commute, mostly tech and business ones', scope: 'fact', ts: Date.now() - DAY * 30, confidence: 0.84, recallCount: 4, lastAccessed: Date.now() - DAY * 1 },
  /* 150 */ { content: 'I do meal prep every Sunday afternoon for the week', scope: 'fact', ts: Date.now() - DAY * 38, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },

  // Personality traits
  /* 151 */ { content: 'I tend to overthink things and get analysis paralysis', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },
  /* 152 */ { content: 'I am an introvert, parties drain me after about 2 hours', scope: 'fact', ts: Date.now() - DAY * 180, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - DAY * 12 },
  /* 153 */ { content: 'I hate being late, I always arrive 10 minutes early', scope: 'preference', ts: Date.now() - DAY * 200, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - DAY * 5 },
  /* 154 */ { content: 'I am a morning person, most productive before noon', scope: 'fact', ts: Date.now() - DAY * 150, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 4 },
  /* 155 */ { content: 'I get road rage easily, trying to work on it', scope: 'fact', ts: Date.now() - DAY * 80, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 156 */ { content: 'I am very organized, color-code my calendar and label everything', scope: 'fact', ts: Date.now() - DAY * 120, confidence: 0.86, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 157 */ { content: 'I cry easily during sad movies, wife teases me about it', scope: 'fact', ts: Date.now() - DAY * 160, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 158 */ { content: 'I procrastinate on household chores but never on work stuff', scope: 'fact', ts: Date.now() - DAY * 90, confidence: 0.84, recallCount: 3, lastAccessed: Date.now() - DAY * 6 },
  /* 159 */ { content: 'I am competitive, even in board games with friends', scope: 'fact', ts: Date.now() - DAY * 110, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },

  // Life events
  /* 160 */ { content: 'I moved from San Francisco to New Jersey 3 years ago for the job at Microsoft', scope: 'fact', ts: Date.now() - DAY * 250, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 18 },
  /* 161 */ { content: 'I changed jobs from a startup to Microsoft because of better work-life balance', scope: 'fact', ts: Date.now() - DAY * 260, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 25 },
  /* 162 */ { content: 'We adopted Luna from a shelter 2 years ago and Mochi was a stray we found', scope: 'fact', ts: Date.now() - DAY * 180, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 10 },
  /* 163 */ { content: 'I got rear-ended on the highway last winter, car needed $3k in repairs', scope: 'episode', ts: Date.now() - DAY * 100, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 25 },
  /* 164 */ { content: 'I went to Tokyo for 2 weeks in 2023, it was my favorite trip ever', scope: 'episode', ts: Date.now() - DAY * 200, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 15 },
  /* 165 */ { content: 'I renovated my kitchen last year, spent about $25k on it', scope: 'episode', ts: Date.now() - DAY * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 166 */ { content: 'I had a job offer from Google but turned it down because of relocation', scope: 'fact', ts: Date.now() - DAY * 130, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 22 },
  /* 167 */ { content: 'I sold my old condo in SF at a loss of $30k because of the market', scope: 'fact', ts: Date.now() - DAY * 240, confidence: 0.84, recallCount: 2, lastAccessed: Date.now() - DAY * 35 },
  /* 168 */ { content: 'My wife and I eloped in Vegas, we had a proper wedding later for family', scope: 'fact', ts: Date.now() - DAY * 350, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 40 },
  /* 169 */ { content: 'I got my first gray hairs at 28, now I just let them be', scope: 'fact', ts: Date.now() - DAY * 170, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },

  // More work
  /* 170 */ { content: 'I have a patent pending for a caching algorithm I designed at Microsoft', scope: 'fact', ts: Date.now() - DAY * 80, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 171 */ { content: 'I failed a system design interview at Meta two years ago', scope: 'fact', ts: Date.now() - DAY * 220, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 35 },

  // More social
  /* 172 */ { content: 'My wife and I take a dance class on Thursday evenings, salsa', scope: 'fact', ts: Date.now() - DAY * 22, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 3 },
  /* 173 */ { content: 'I am in a book club with 6 people, we meet monthly at the library', scope: 'fact', ts: Date.now() - DAY * 55, confidence: 0.84, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },

  // More travel
  /* 174 */ { content: 'I have been to 14 countries total, hoping to reach 20 by 40', scope: 'fact', ts: Date.now() - DAY * 110, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 175 */ { content: 'I got my passport renewed last month, valid until 2036', scope: 'fact', ts: Date.now() - DAY * 5, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - DAY * 2 },

  // More home
  /* 176 */ { content: 'We live in a 3-bedroom house in Hoboken, New Jersey', scope: 'fact', ts: Date.now() - DAY * 250, confidence: 0.92, recallCount: 4, lastAccessed: Date.now() - DAY * 3 },
  /* 177 */ { content: 'Our house has a small backyard with a grill and a fire pit', scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 8 },
  /* 178 */ { content: 'We are thinking about getting solar panels installed', scope: 'fact', ts: Date.now() - DAY * 4, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - DAY * 1 },

  // More preferences
  /* 179 */ { content: 'I prefer window seats on planes', scope: 'preference', ts: Date.now() - DAY * 140, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - DAY * 15 },
  /* 180 */ { content: 'I hate small talk, prefer deep conversations', scope: 'preference', ts: Date.now() - DAY * 170, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - DAY * 10 },
  /* 181 */ { content: 'I always sleep on the left side of the bed', scope: 'preference', ts: Date.now() - DAY * 180, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 5 },
  /* 182 */ { content: 'I prefer paper books over Kindle, I like the feel', scope: 'preference', ts: Date.now() - DAY * 130, confidence: 0.84, recallCount: 3, lastAccessed: Date.now() - DAY * 6 },

  // More random life details
  /* 183 */ { content: 'I keep a sourdough starter named Bready Mercury', scope: 'fact', ts: Date.now() - DAY * 40, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - DAY * 5 },
  /* 184 */ { content: 'My shoe size is 10.5 US', scope: 'fact', ts: Date.now() - DAY * 200, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 25 },
  /* 185 */ { content: 'I am 5 foot 11 and weigh about 175 pounds', scope: 'fact', ts: Date.now() - DAY * 60, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 15 },
  /* 186 */ { content: 'I have been considering therapy for my anxiety but have not started yet', scope: 'fact', ts: Date.now() - DAY * 10, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 3 },
  /* 187 */ { content: 'I wear glasses for reading but contacts for everything else', scope: 'fact', ts: Date.now() - DAY * 100, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 8 },
  /* 188 */ { content: 'My favorite color is navy blue', scope: 'preference', ts: Date.now() - DAY * 220, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },
  /* 189 */ { content: 'I have a birthmark on my right shoulder', scope: 'fact', ts: Date.now() - DAY * 300, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - DAY * 50 },
  /* 190 */ { content: 'I am left-handed', scope: 'fact', ts: Date.now() - DAY * 300, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - DAY * 15 },
  /* 191 */ { content: 'I hate the sound of chewing, it drives me crazy', scope: 'fact', ts: Date.now() - DAY * 180, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 192 */ { content: 'I was born on July 14, 1992', scope: 'fact', ts: Date.now() - DAY * 400, confidence: 0.95, recallCount: 2, lastAccessed: Date.now() - DAY * 20 },
  /* 193 */ { content: 'I speak conversational French from my time in Berlin (had French roommates)', scope: 'fact', ts: Date.now() - DAY * 350, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - DAY * 30 },
  /* 194 */ { content: 'I had a Labrador named Buddy growing up, he passed when I was 15', scope: 'fact', ts: Date.now() - DAY * 350, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - DAY * 40 },
  /* 195 */ { content: 'I am the middle child of three, older brother and younger sister', scope: 'fact', ts: Date.now() - DAY * 300, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - DAY * 15 },
  /* 196 */ { content: 'I bought a standing desk converter for my home office for $400', scope: 'fact', ts: Date.now() - DAY * 45, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - DAY * 10 },
  /* 197 */ { content: 'I have a recurring nightmare about being chased through a dark forest', scope: 'fact', ts: Date.now() - DAY * 80, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - DAY * 12 },
  /* 198 */ { content: 'My favorite holiday is Christmas because the whole family gets together', scope: 'preference', ts: Date.now() - DAY * 200, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - DAY * 30 },
  /* 199 */ { content: 'I have been thinking about starting a YouTube channel about cooking', scope: 'fact', ts: Date.now() - DAY * 3, confidence: 0.75, recallCount: 1, lastAccessed: Date.now() - DAY * 1 },
] as Memory[]

// ═══════════════════════════════════════════════════════════════
// TEST QUERIES: 500 queries (200 direct + 200 semantic + 100 hard)
// ═══════════════════════════════════════════════════════════════

interface TestCase {
  query: string
  expectedIndex: number | number[]  // single index or array (multi-match: pass if ANY hit)
  type: 'direct' | 'semantic' | 'hard'
  description: string
}

const TEST_CASES: TestCase[] = [
  // ══════════════════════════════════════════════════════════════
  // ── Direct queries (200) ─────────────────────────────────────
  // ══════════════════════════════════════════════════════════════

  // Original 40 direct
  { query: 'What time do I wake up', expectedIndex: [0, 42], type: 'direct', description: 'wake up → 6am / 5:30am' },
  { query: 'What am I allergic to', expectedIndex: [1, 62], type: 'direct', description: 'allergic → shellfish / peanut' },
  { query: 'What car do I drive', expectedIndex: 2, type: 'direct', description: 'car → BMW' },
  { query: "What's my job title", expectedIndex: 3, type: 'direct', description: 'job title → senior eng' },
  { query: 'What sport does my son play', expectedIndex: 4, type: 'direct', description: 'son sport → soccer' },
  { query: 'How long since I quit drinking', expectedIndex: 5, type: 'direct', description: 'quit drinking → 3mo' },
  { query: 'What am I afraid of', expectedIndex: [6, 50, 77], type: 'direct', description: 'afraid → heights/spiders/speaking' },
  { query: 'Where am I traveling next', expectedIndex: 7, type: 'direct', description: 'travel → Italy' },
  { query: 'Where does my roommate Kevin work', expectedIndex: 8, type: 'direct', description: 'Kevin → Google' },
  { query: "What's my blood type", expectedIndex: 9, type: 'direct', description: 'blood type → A+' },
  { query: 'What do I do before bed', expectedIndex: [10, 45], type: 'direct', description: 'before bed → read / journal' },
  { query: 'What degree am I considering', expectedIndex: 11, type: 'direct', description: 'degree → MBA' },
  { query: 'How much did I lose in crypto', expectedIndex: 12, type: 'direct', description: 'crypto → $5000' },
  { query: 'What language am I learning', expectedIndex: 13, type: 'direct', description: 'language → Spanish' },
  { query: 'How did I meet my wife', expectedIndex: 14, type: 'direct', description: 'meet wife → dating app' },
  { query: 'What laptop do I use', expectedIndex: 15, type: 'direct', description: 'laptop → ThinkPad' },
  { query: 'What sport do I play on Wednesdays', expectedIndex: 16, type: 'direct', description: 'Wednesday → basketball' },
  { query: 'What book am I reading', expectedIndex: 17, type: 'direct', description: 'book → Sapiens' },
  { query: 'What surgery have I had', expectedIndex: 18, type: 'direct', description: 'surgery → knee' },
  { query: 'Where do I work', expectedIndex: 19, type: 'direct', description: 'work → Microsoft' },
  { query: "When is my daughter's birthday", expectedIndex: 20, type: 'direct', description: 'daughter bday → Mar 15' },
  { query: 'Which programming language do I prefer', expectedIndex: 21, type: 'direct', description: 'prefer → Python' },
  { query: 'How much is my mortgage', expectedIndex: 22, type: 'direct', description: 'mortgage → $2500' },
  { query: 'Do I meditate', expectedIndex: 23, type: 'direct', description: 'meditate → yes 20min' },
  { query: 'Where does my mom live', expectedIndex: 24, type: 'direct', description: 'mom → Chicago' },
  { query: 'What am I training for', expectedIndex: 25, type: 'direct', description: 'training → half marathon' },
  { query: 'iPhone or Android', expectedIndex: 26, type: 'direct', description: 'phone → Android' },
  { query: "What are my cats' names", expectedIndex: 27, type: 'direct', description: 'cats → Luna & Mochi' },
  { query: "What's my favorite restaurant", expectedIndex: 28, type: 'direct', description: 'restaurant → Italian 5th' },
  { query: 'What health issue do I have', expectedIndex: [29, 18, 55], type: 'direct', description: 'health → back/knee/arm' },
  { query: 'What do I do on Sundays', expectedIndex: [30, 44], type: 'direct', description: 'Sundays → food bank / FaceTime sister' },
  { query: 'How big is my team', expectedIndex: 31, type: 'direct', description: 'team → 8 people' },
  { query: 'How do I commute', expectedIndex: 32, type: 'direct', description: 'commute → train 45min' },
  { query: 'Am I looking to buy property', expectedIndex: 33, type: 'direct', description: 'property → yes' },
  { query: 'Who is my best friend', expectedIndex: 34, type: 'direct', description: 'best friend → Dave' },
  { query: 'What diet do I follow', expectedIndex: [35, 43], type: 'direct', description: 'diet → IF 16:8 / vegetarian' },
  { query: 'Where was my last vacation', expectedIndex: 36, type: 'direct', description: 'vacation → Bali' },
  { query: 'Am I mentoring anyone', expectedIndex: 37, type: 'direct', description: 'mentoring → 2 juniors' },
  { query: 'When is my annual review', expectedIndex: 38, type: 'direct', description: 'review → December' },
  { query: "What's my side project", expectedIndex: 39, type: 'direct', description: 'side project → recipe app' },

  // Direct for memories 40–79
  { query: 'Do I drink regular milk', expectedIndex: 40, type: 'direct', description: 'milk → oat milk' },
  { query: "What's my favorite TV show", expectedIndex: 41, type: 'direct', description: 'TV show → Breaking Bad' },
  { query: 'What time do I go to the gym', expectedIndex: 42, type: 'direct', description: 'gym time → 5:30am' },
  { query: 'Am I vegetarian', expectedIndex: 43, type: 'direct', description: 'vegetarian → yes 3 years' },
  { query: 'Where does my sister live', expectedIndex: 44, type: 'direct', description: 'sister → Seattle' },
  { query: 'Do I keep a journal', expectedIndex: 45, type: 'direct', description: 'journal → yes nightly' },
  { query: 'Who is my car insurance with', expectedIndex: 46, type: 'direct', description: 'car insurance → Geico $150' },
  { query: 'What instrument am I learning', expectedIndex: 47, type: 'direct', description: 'instrument → guitar' },
  { query: 'What app do I use for notes', expectedIndex: 48, type: 'direct', description: 'notes → Notion' },
  { query: 'What did I want to be as a kid', expectedIndex: 49, type: 'direct', description: 'childhood dream → astronaut' },
  { query: 'Am I scared of spiders', expectedIndex: 50, type: 'direct', description: 'spiders → yes' },
  { query: 'What charity do I donate to', expectedIndex: 51, type: 'direct', description: 'charity → Red Cross' },
  { query: 'What cuisine do I like most', expectedIndex: 52, type: 'direct', description: 'cuisine → Thai' },
  { query: 'Do I have a standing desk', expectedIndex: 53, type: 'direct', description: 'standing desk → yes' },
  { query: 'How much screen time am I targeting', expectedIndex: 54, type: 'direct', description: 'screen time → under 3hr' },
  { query: 'Have I ever broken a bone', expectedIndex: 55, type: 'direct', description: 'broken bone → arm football' },
  { query: "Does my neighbor's dog bother me", expectedIndex: 56, type: 'direct', description: 'neighbor dog → barks 6am' },
  { query: 'What streaming services do I have', expectedIndex: 57, type: 'direct', description: 'streaming → Netflix/Disney+/HBO' },
  { query: 'Am I planning to propose', expectedIndex: 58, type: 'direct', description: 'propose → September' },
  { query: 'Who taught me to make pasta', expectedIndex: 59, type: 'direct', description: 'pasta → grandma' },
  { query: 'How often do I run', expectedIndex: [25, 60], type: 'direct', description: 'running → 5K Tue/Thu + marathon' },
  { query: 'What does my brother do', expectedIndex: 61, type: 'direct', description: 'brother → dentist Portland' },
  { query: 'Do I carry an EpiPen', expectedIndex: 62, type: 'direct', description: 'EpiPen → peanut allergy' },
  { query: "What's my favorite band", expectedIndex: 63, type: 'direct', description: 'band → Radiohead' },
  { query: 'What supplements do I take', expectedIndex: 64, type: 'direct', description: 'supplements → vitamin D + omega-3' },
  { query: 'What car am I saving for', expectedIndex: 65, type: 'direct', description: 'saving → Tesla Model 3' },
  { query: "Did I coach my daughter's team", expectedIndex: 66, type: 'direct', description: 'coaching → daughter soccer' },
  { query: 'Do I have any tattoos', expectedIndex: 67, type: 'direct', description: 'tattoo → compass forearm' },
  { query: 'Did I pass my driving test first try', expectedIndex: 68, type: 'direct', description: 'driving test → failed first' },
  { query: 'Where is my WiFi password', expectedIndex: 69, type: 'direct', description: 'WiFi → under router' },
  { query: 'Do I like hot sauce', expectedIndex: 70, type: 'direct', description: 'hot sauce → extra on burrito' },
  { query: 'Did I do a coding bootcamp', expectedIndex: 71, type: 'direct', description: 'bootcamp → before CS degree' },
  { query: 'Am I getting a dog', expectedIndex: 72, type: 'direct', description: 'dog → golden retriever waitlist' },
  { query: 'Do I use a white noise machine', expectedIndex: 73, type: 'direct', description: 'white noise → yes' },
  { query: 'Have I had food poisoning recently', expectedIndex: 74, type: 'direct', description: 'food poisoning → sushi' },
  { query: "What's my favorite movie", expectedIndex: 75, type: 'direct', description: 'movie → Shawshank' },
  { query: 'Did I max out my 401k', expectedIndex: 76, type: 'direct', description: '401k → maxed out' },
  { query: 'Am I afraid of public speaking', expectedIndex: 77, type: 'direct', description: 'public speaking → yes' },
  { query: 'Did I build something for my kids', expectedIndex: 78, type: 'direct', description: 'built → treehouse' },
  { query: 'What do I order at the coffee shop', expectedIndex: 79, type: 'direct', description: 'coffee → flat white oat milk' },

  // New direct queries for memories 80–199
  { query: 'What is Project Aurora', expectedIndex: 80, type: 'direct', description: 'Project Aurora → cloud migration' },
  { query: 'What tech stack do I use at work', expectedIndex: 81, type: 'direct', description: 'tech stack → React/TS/Azure' },
  { query: 'Who brings donuts on Fridays', expectedIndex: 82, type: 'direct', description: 'donuts → Sarah' },
  { query: 'What did I get on my performance review', expectedIndex: 83, type: 'direct', description: 'perf review → exceeds expectations' },
  { query: 'What project management tool does my team use', expectedIndex: 84, type: 'direct', description: 'PM tool → Jira' },
  { query: 'Who is my manager', expectedIndex: 85, type: 'direct', description: 'manager → Tom from Amazon' },
  { query: 'Did I present at the all-hands meeting', expectedIndex: 86, type: 'direct', description: 'all-hands → yes last quarter' },
  { query: 'Where is the team offsite', expectedIndex: 87, type: 'direct', description: 'offsite → Austin' },
  { query: 'How many PTO days do I have left', expectedIndex: 88, type: 'direct', description: 'PTO → 18 days' },
  { query: 'How much RAM does my work laptop have', expectedIndex: 89, type: 'direct', description: 'laptop RAM → 32GB' },
  { query: 'How much was my bonus', expectedIndex: 90, type: 'direct', description: 'bonus → $15k' },
  { query: 'When are our standup meetings', expectedIndex: 91, type: 'direct', description: 'standup → 9:30am Teams' },
  { query: 'What did my dad do for a living', expectedIndex: 92, type: 'direct', description: 'dad → retired math teacher' },
  { query: 'What was my mom\'s career', expectedIndex: 93, type: 'direct', description: 'mom career → nurse 30 years' },
  { query: 'Is my sister getting married', expectedIndex: 94, type: 'direct', description: 'sister wedding → October' },
  { query: 'What do we do for Thanksgiving', expectedIndex: 95, type: 'direct', description: 'Thanksgiving → family reunion' },
  { query: 'What grade is my son in', expectedIndex: 96, type: 'direct', description: 'son grade → 3rd Lincoln Elementary' },
  { query: 'What does my wife do for work', expectedIndex: 97, type: 'direct', description: 'wife job → interior designer' },
  { query: 'What did my father-in-law do', expectedIndex: 98, type: 'direct', description: 'father-in-law → Army colonel' },
  { query: 'When was my parents anniversary', expectedIndex: 99, type: 'direct', description: 'parents anniversary → 40th last year' },
  { query: 'What does my daughter want to be', expectedIndex: 100, type: 'direct', description: 'daughter career → vet' },
  { query: 'Does my uncle have a vineyard', expectedIndex: 101, type: 'direct', description: 'uncle vineyard → Napa' },
  { query: 'Do I have asthma', expectedIndex: 102, type: 'direct', description: 'asthma → mild + inhaler' },
  { query: 'What do I take for sleep', expectedIndex: 103, type: 'direct', description: 'sleep aid → melatonin 10mg' },
  { query: 'Do I need to check my cholesterol', expectedIndex: 104, type: 'direct', description: 'cholesterol → every 6 months' },
  { query: 'When did I get my wisdom teeth out', expectedIndex: 105, type: 'direct', description: 'wisdom teeth → age 20' },
  { query: 'Do I wear contacts', expectedIndex: 106, type: 'direct', description: 'contacts → -3.5 both eyes' },
  { query: 'Do I see a chiropractor', expectedIndex: 107, type: 'direct', description: 'chiropractor → every 2 weeks' },
  { query: 'When is my dental appointment', expectedIndex: 108, type: 'direct', description: 'dental → next Tuesday' },
  { query: 'What is my resting heart rate', expectedIndex: 109, type: 'direct', description: 'heart rate → 58 bpm' },
  { query: 'Did I have a concussion', expectedIndex: 110, type: 'direct', description: 'concussion → football high school' },
  { query: 'How do I invest my money', expectedIndex: 111, type: 'direct', description: 'invest → 70% index funds' },
  { query: 'What is my salary', expectedIndex: 112, type: 'direct', description: 'salary → $165k' },
  { query: 'Do I have life insurance', expectedIndex: 113, type: 'direct', description: 'life insurance → $500k NW Mutual' },
  { query: 'How much do I owe on my car', expectedIndex: 114, type: 'direct', description: 'car loan → $28k' },
  { query: 'How do I file my taxes', expectedIndex: 115, type: 'direct', description: 'taxes → TurboTax $2k refund' },
  { query: 'Do I have a Roth IRA', expectedIndex: 116, type: 'direct', description: 'Roth IRA → yes' },
  { query: 'What is my credit score', expectedIndex: 117, type: 'direct', description: 'credit score → 780' },
  { query: 'Do I have an emergency fund', expectedIndex: 118, type: 'direct', description: 'emergency fund → 6 months' },
  { query: 'When is poker night', expectedIndex: 119, type: 'direct', description: 'poker → first Friday monthly' },
  { query: 'Did I throw a surprise party for my wife', expectedIndex: 120, type: 'direct', description: 'surprise party → rooftop bar' },
  { query: 'Who just moved back from Japan', expectedIndex: 121, type: 'direct', description: 'Japan → Mike' },
  { query: 'Did I see Dave in London', expectedIndex: 122, type: 'direct', description: 'Dave London → conference' },
  { query: 'Do we have a neighborhood BBQ', expectedIndex: 123, type: 'direct', description: 'BBQ → 4th of July' },
  { query: 'Who is Lisa', expectedIndex: 124, type: 'direct', description: 'Lisa → sommelier friend' },
  { query: 'Did I host a game night', expectedIndex: 125, type: 'direct', description: 'game night → last weekend 12 people' },
  { query: 'Do I have a college group chat', expectedIndex: 126, type: 'direct', description: 'group chat → yes active' },
  { query: 'Where did I go to college', expectedIndex: 127, type: 'direct', description: 'college → U of Michigan CS 2016' },
  { query: 'Who was my favorite professor', expectedIndex: 128, type: 'direct', description: 'professor → Dr. Chen algorithms' },
  { query: 'What class did I almost fail', expectedIndex: 129, type: 'direct', description: 'almost failed → organic chemistry' },
  { query: 'Did I win a hackathon', expectedIndex: 130, type: 'direct', description: 'hackathon → 2015 CS club' },
  { query: 'What was my senior thesis about', expectedIndex: 131, type: 'direct', description: 'thesis → distributed systems' },
  { query: 'Did I have a scholarship', expectedIndex: 132, type: 'direct', description: 'scholarship → 50% tuition' },
  { query: 'Did I study abroad', expectedIndex: 133, type: 'direct', description: 'study abroad → Berlin' },
  { query: 'Was I a teaching assistant', expectedIndex: 134, type: 'direct', description: 'TA → intro programming senior year' },
  { query: 'Did I finish a puzzle recently', expectedIndex: 135, type: 'direct', description: 'puzzle → Starry Night 1000 pieces' },
  { query: 'Do I brew beer', expectedIndex: 136, type: 'direct', description: 'brew beer → IPA at home' },
  { query: 'What was my half marathon time', expectedIndex: 137, type: 'direct', description: 'marathon time → 1:52' },
  { query: 'Do I collect vinyl records', expectedIndex: 138, type: 'direct', description: 'vinyl → 200 records' },
  { query: 'Do I do woodworking', expectedIndex: 139, type: 'direct', description: 'woodworking → bookshelf' },
  { query: 'Did I enter a photography contest', expectedIndex: 140, type: 'direct', description: 'photo contest → 3rd place sunset' },
  { query: 'What do I grow in my garden', expectedIndex: 141, type: 'direct', description: 'garden → tomatoes basil peppers' },
  { query: 'What is my chess rating', expectedIndex: 142, type: 'direct', description: 'chess → 1200 chess.com' },
  { query: 'What train do I take to work', expectedIndex: 143, type: 'direct', description: 'train → 7:15am Hoboken to Penn' },
  { query: 'What do I eat for lunch', expectedIndex: 144, type: 'direct', description: 'lunch → Sweetgreen salad 12:30' },
  { query: 'When do I pick up my son from soccer', expectedIndex: 145, type: 'direct', description: 'pickup → 5pm Saturday' },
  { query: 'How do I make coffee at home', expectedIndex: 146, type: 'direct', description: 'coffee home → Chemex pour-over' },
  { query: 'What time do I get home from work', expectedIndex: 147, type: 'direct', description: 'home time → 7pm' },
  { query: 'Do I walk my cats', expectedIndex: 148, type: 'direct', description: 'walk cats → 8pm Luna loves Mochi sits' },
  { query: 'What do I listen to on my commute', expectedIndex: 149, type: 'direct', description: 'commute audio → podcasts tech/business' },
  { query: 'Do I meal prep', expectedIndex: 150, type: 'direct', description: 'meal prep → Sunday afternoon' },
  { query: 'Do I overthink things', expectedIndex: 151, type: 'direct', description: 'overthink → analysis paralysis' },
  { query: 'Am I an introvert or extrovert', expectedIndex: 152, type: 'direct', description: 'introvert → parties drain 2hr' },
  { query: 'Am I punctual', expectedIndex: 153, type: 'direct', description: 'punctual → 10 min early always' },
  { query: 'Am I a morning person', expectedIndex: 154, type: 'direct', description: 'morning person → productive before noon' },
  { query: 'Do I have road rage', expectedIndex: 155, type: 'direct', description: 'road rage → yes working on it' },
  { query: 'Am I organized', expectedIndex: 156, type: 'direct', description: 'organized → color-code calendar' },
  { query: 'Do I cry at movies', expectedIndex: 157, type: 'direct', description: 'cry movies → yes wife teases' },
  { query: 'Do I procrastinate', expectedIndex: 158, type: 'direct', description: 'procrastinate → chores not work' },
  { query: 'Am I competitive', expectedIndex: 159, type: 'direct', description: 'competitive → even board games' },
  { query: 'Where did I live before New Jersey', expectedIndex: 160, type: 'direct', description: 'before NJ → San Francisco' },
  { query: 'Why did I leave my old job', expectedIndex: 161, type: 'direct', description: 'left job → work-life balance' },
  { query: 'How did I get my cats', expectedIndex: 162, type: 'direct', description: 'cats origin → shelter + stray' },
  { query: 'Did I get in a car accident', expectedIndex: 163, type: 'direct', description: 'accident → rear-ended $3k' },
  { query: 'Have I been to Tokyo', expectedIndex: 164, type: 'direct', description: 'Tokyo → 2 weeks 2023 favorite' },
  { query: 'Did I renovate my kitchen', expectedIndex: 165, type: 'direct', description: 'kitchen → $25k renovation' },
  { query: 'Did Google offer me a job', expectedIndex: 166, type: 'direct', description: 'Google offer → turned down relocation' },
  { query: 'Did I sell my condo in SF', expectedIndex: 167, type: 'direct', description: 'SF condo → sold at $30k loss' },
  { query: 'How did I get married', expectedIndex: 168, type: 'direct', description: 'married → eloped Vegas + proper wedding' },
  { query: 'When did I get gray hair', expectedIndex: 169, type: 'direct', description: 'gray hair → 28' },
  { query: 'Do I have any patents', expectedIndex: 170, type: 'direct', description: 'patent → caching algorithm' },
  { query: 'Did I interview at Meta', expectedIndex: 171, type: 'direct', description: 'Meta → failed system design' },
  { query: 'What dance class do I take', expectedIndex: 172, type: 'direct', description: 'dance → salsa Thursday' },
  { query: 'Am I in a book club', expectedIndex: 173, type: 'direct', description: 'book club → 6 people monthly library' },
  { query: 'How many countries have I visited', expectedIndex: 174, type: 'direct', description: 'countries → 14, goal 20 by 40' },
  { query: 'When does my passport expire', expectedIndex: 175, type: 'direct', description: 'passport → 2036' },
  { query: 'Where do I live', expectedIndex: 176, type: 'direct', description: 'home → 3BR Hoboken NJ' },
  { query: 'Do I have a backyard', expectedIndex: 177, type: 'direct', description: 'backyard → grill + fire pit' },
  { query: 'Am I considering solar panels', expectedIndex: 178, type: 'direct', description: 'solar → thinking about it' },
  { query: 'Window or aisle seat', expectedIndex: 179, type: 'direct', description: 'seat → window' },
  { query: 'Do I like small talk', expectedIndex: 180, type: 'direct', description: 'small talk → hate it' },
  { query: 'Which side of the bed do I sleep on', expectedIndex: 181, type: 'direct', description: 'bed → left side' },
  { query: 'Do I prefer Kindle or paper books', expectedIndex: 182, type: 'direct', description: 'books → paper' },
  { query: 'Do I have a sourdough starter', expectedIndex: 183, type: 'direct', description: 'sourdough → Bready Mercury' },
  { query: 'What is my shoe size', expectedIndex: 184, type: 'direct', description: 'shoe → 10.5 US' },
  { query: 'How tall am I', expectedIndex: 185, type: 'direct', description: 'height → 5\'11 175lbs' },
  { query: 'Am I considering therapy', expectedIndex: 186, type: 'direct', description: 'therapy → anxiety not started' },
  { query: 'What is my favorite color', expectedIndex: 188, type: 'direct', description: 'color → navy blue' },
  { query: 'Do I have a birthmark', expectedIndex: 189, type: 'direct', description: 'birthmark → right shoulder' },
  { query: 'Am I left-handed or right-handed', expectedIndex: 190, type: 'direct', description: 'handedness → left' },
  { query: 'Does chewing bother me', expectedIndex: 191, type: 'direct', description: 'chewing → misophonia' },
  { query: 'When is my birthday', expectedIndex: 192, type: 'direct', description: 'birthday → July 14 1992' },
  { query: 'Do I speak French', expectedIndex: 193, type: 'direct', description: 'French → conversational' },
  { query: 'Did I have a dog as a kid', expectedIndex: 194, type: 'direct', description: 'childhood dog → Buddy Labrador' },
  { query: 'Am I the oldest sibling', expectedIndex: 195, type: 'direct', description: 'sibling order → middle child' },
  { query: 'How much did my standing desk cost', expectedIndex: 196, type: 'direct', description: 'standing desk → $400' },
  { query: 'Do I have nightmares', expectedIndex: 197, type: 'direct', description: 'nightmare → chased dark forest' },
  { query: 'What is my favorite holiday', expectedIndex: 198, type: 'direct', description: 'holiday → Christmas family' },
  { query: 'Am I thinking about starting a YouTube channel', expectedIndex: 199, type: 'direct', description: 'YouTube → cooking channel' },

  // ══════════════════════════════════════════════════════════════
  // ── Semantic queries (200) ───────────────────────────────────
  // ══════════════════════════════════════════════════════════════

  // Original semantic (updated for new memories)
  { query: 'my morning routine', expectedIndex: [0, 23, 42, 60, 146], type: 'semantic', description: 'morning → 6am + meditate + gym + run + coffee' },
  { query: 'my food restrictions', expectedIndex: [1, 43, 62], type: 'semantic', description: 'food restrict → shellfish/veg/peanut' },
  { query: 'my vehicle', expectedIndex: [2, 65], type: 'semantic', description: 'vehicle → BMW / saving Tesla' },
  { query: 'my career progress', expectedIndex: [3, 83, 90], type: 'semantic', description: 'career → promoted / review / bonus' },
  { query: "my kid's activities", expectedIndex: [4, 66], type: 'semantic', description: 'kid activities → soccer / coaching' },
  { query: "addictions I've overcome", expectedIndex: 5, type: 'semantic', description: 'addiction → quit drinking' },
  { query: 'my phobias', expectedIndex: [6, 50, 77], type: 'semantic', description: 'phobias → heights/spiders/speaking' },
  { query: 'upcoming travel plans', expectedIndex: [7, 87], type: 'semantic', description: 'travel plans → Italy / Austin offsite' },
  { query: 'old friends from school', expectedIndex: [8, 121, 126], type: 'semantic', description: 'old friends → Kevin / Mike / group chat' },
  { query: 'my health profile', expectedIndex: [9, 18, 29, 55, 62, 102], type: 'semantic', description: 'health → blood/knee/back/arm/peanut/asthma' },
  { query: 'my nighttime habits', expectedIndex: [10, 45, 73], type: 'semantic', description: 'nighttime → reading/journal/white noise' },
  { query: 'my education plans', expectedIndex: [11, 71], type: 'semantic', description: 'education → MBA / bootcamp' },
  { query: 'my investment losses', expectedIndex: [12, 167], type: 'semantic', description: 'investment loss → crypto / SF condo' },
  { query: 'self improvement efforts', expectedIndex: [13, 37, 47, 54], type: 'semantic', description: 'self improve → Spanish/mentor/guitar/screen' },
  { query: 'my love story', expectedIndex: [14, 58, 168], type: 'semantic', description: 'love → dating app / propose / eloped' },
  { query: 'my work setup', expectedIndex: [15, 53, 89], type: 'semantic', description: 'work setup → ThinkPad / standing desk / 32GB' },
  { query: 'my weekly exercise', expectedIndex: [16, 25, 42, 60], type: 'semantic', description: 'exercise → basketball/marathon/gym/5K' },
  { query: "what I'm reading lately", expectedIndex: [17, 173], type: 'semantic', description: 'reading → Sapiens / book club' },
  { query: 'past medical procedures', expectedIndex: [18, 105, 110], type: 'semantic', description: 'medical → knee surgery / wisdom teeth / concussion' },
  { query: 'my employer', expectedIndex: 19, type: 'semantic', description: 'employer → Microsoft' },
  { query: 'important family dates', expectedIndex: [20, 58, 94, 99], type: 'semantic', description: 'family dates → Mar 15 / propose / sister wedding / anniversary' },
  { query: 'my tech stack preferences', expectedIndex: [21, 81], type: 'semantic', description: 'tech stack → Python / React+TS+Azure' },
  { query: 'my monthly expenses', expectedIndex: [22, 46, 57], type: 'semantic', description: 'expenses → mortgage/insurance/streaming' },
  { query: 'my wellness practices', expectedIndex: [23, 35, 64, 107], type: 'semantic', description: 'wellness → meditation/fasting/supplements/chiro' },
  { query: "my family's locations", expectedIndex: [24, 44, 61, 176], type: 'semantic', description: 'family loc → Chicago/Seattle/Portland/Hoboken' },
  { query: 'my fitness goals', expectedIndex: [25, 42, 60, 137], type: 'semantic', description: 'fitness → marathon/gym/5K/half marathon time' },
  { query: 'my phone choice', expectedIndex: 26, type: 'semantic', description: 'phone → Android' },
  { query: 'my pets', expectedIndex: [27, 72, 162], type: 'semantic', description: 'pets → cats / puppy waitlist / adoption' },
  { query: 'my dining preferences', expectedIndex: [28, 52, 70], type: 'semantic', description: 'dining → Italian/Thai/hot sauce' },
  { query: 'chronic health issues', expectedIndex: [29, 18, 102], type: 'semantic', description: 'chronic → back pain / knee / asthma' },
  { query: 'my community involvement', expectedIndex: [30, 51], type: 'semantic', description: 'community → food bank / Red Cross' },
  { query: 'my work environment', expectedIndex: [31, 37, 84, 91], type: 'semantic', description: 'work env → team 8 / mentoring / Jira / standups' },
  { query: 'my daily commute', expectedIndex: [32, 143, 149], type: 'semantic', description: 'daily commute → train / 7:15 / podcasts' },
  { query: 'major financial decisions ahead', expectedIndex: [33, 65, 178], type: 'semantic', description: 'financial → house / Tesla / solar' },
  { query: 'closest friendships', expectedIndex: [34, 121, 122], type: 'semantic', description: 'friendships → Dave / Mike / London' },
  { query: 'my eating habits', expectedIndex: [35, 43, 40, 144], type: 'semantic', description: 'eating → IF/vegetarian/oat milk/Sweetgreen' },
  { query: 'best travel memories', expectedIndex: [36, 164], type: 'semantic', description: 'travel memories → Bali / Tokyo' },
  { query: 'my leadership role', expectedIndex: [37, 66, 134], type: 'semantic', description: 'leadership → mentoring / coaching / TA' },
  { query: 'upcoming work milestones', expectedIndex: [38, 87], type: 'semantic', description: 'milestones → review Dec / offsite Austin' },
  { query: 'my hobby projects', expectedIndex: [39, 47, 136, 139], type: 'semantic', description: 'hobby → recipe app / guitar / brew / woodwork' },

  // More semantic (new)
  { query: 'what don\'t I eat', expectedIndex: [43, 1, 62], type: 'semantic', description: 'don\'t eat → vegetarian/shellfish/peanut' },
  { query: 'my fears and anxieties', expectedIndex: [6, 50, 77, 186], type: 'semantic', description: 'fears → heights/spiders/speaking/anxiety' },
  { query: 'tell me about my family', expectedIndex: [24, 44, 61, 20, 66, 92, 93, 97], type: 'semantic', description: 'family → mom/sister/brother/daughter/dad/wife' },
  { query: 'my health history', expectedIndex: [18, 29, 55, 9, 62, 102, 110], type: 'semantic', description: 'health hist → knee/back/arm/blood/peanut/asthma/concussion' },
  { query: 'what have I been doing recently', expectedIndex: [13, 17, 25, 47, 58, 135], type: 'semantic', description: 'recently → Spanish/Sapiens/marathon/guitar/propose/puzzle' },
  { query: 'all my recurring expenses', expectedIndex: [22, 46, 57, 113], type: 'semantic', description: 'recurring $ → mortgage/insurance/streaming/life ins' },
  { query: 'my relationship milestones', expectedIndex: [14, 58, 168], type: 'semantic', description: 'relationship → met wife / proposing / eloped' },
  { query: 'what I do for exercise', expectedIndex: [16, 25, 42, 60], type: 'semantic', description: 'exercise → basketball/marathon/gym/5K' },
  { query: 'things I do every day', expectedIndex: [0, 23, 35, 42, 45, 64, 146], type: 'semantic', description: 'daily → wake/meditate/fast/gym/journal/supps/coffee' },
  { query: 'my entertainment and media', expectedIndex: [41, 57, 63, 75], type: 'semantic', description: 'entertainment → BB/streaming/Radiohead/Shawshank' },
  { query: 'dairy-free choices', expectedIndex: [40, 79], type: 'semantic', description: 'dairy free → oat milk / flat white oat' },
  { query: 'things that annoy me', expectedIndex: [50, 56, 191], type: 'semantic', description: 'annoy → spiders / neighbor dog / chewing' },
  { query: 'my learning journey', expectedIndex: [13, 47, 71, 127], type: 'semantic', description: 'learning → Spanish/guitar/bootcamp/college' },
  { query: 'my sleep routine', expectedIndex: [10, 45, 73, 103], type: 'semantic', description: 'sleep → read/journal/white noise/melatonin' },
  { query: 'bad experiences I\'ve had', expectedIndex: [50, 68, 74, 12, 163], type: 'semantic', description: 'bad exp → spiders/driving/sushi/crypto/accident' },
  { query: 'people I care about', expectedIndex: [14, 24, 34, 44, 61, 97], type: 'semantic', description: 'people → wife/mom/Dave/sister/brother/wife' },
  { query: 'how I give back to others', expectedIndex: [30, 37, 51, 66], type: 'semantic', description: 'give back → food bank/mentor/donate/coach' },
  { query: 'my cooking skills', expectedIndex: [59, 136, 183], type: 'semantic', description: 'cooking → grandma pasta / brew beer / sourdough' },
  { query: 'my digital tools and apps', expectedIndex: [48, 15, 84], type: 'semantic', description: 'digital tools → Notion / ThinkPad / Jira' },
  { query: 'what I watch on TV', expectedIndex: [41, 57], type: 'semantic', description: 'watch TV → Breaking Bad / streaming' },
  { query: 'injuries and accidents', expectedIndex: [18, 29, 55, 110, 163], type: 'semantic', description: 'injuries → knee/back/arm/concussion/car accident' },
  { query: 'my body modifications', expectedIndex: 67, type: 'semantic', description: 'body mod → compass tattoo' },
  { query: 'things I failed at', expectedIndex: [12, 68, 129, 171], type: 'semantic', description: 'failures → crypto/driving/orgo chem/Meta interview' },
  { query: 'my savings and investments', expectedIndex: [65, 76, 111, 116, 118], type: 'semantic', description: 'savings → Tesla/401k/index funds/Roth/emergency' },
  { query: 'musical interests', expectedIndex: [47, 63, 138], type: 'semantic', description: 'music → guitar / Radiohead / vinyl' },
  { query: 'animals in my life', expectedIndex: [27, 72, 56, 162, 194], type: 'semantic', description: 'animals → cats/puppy/neighbor dog/adoption/Buddy' },
  { query: 'my childhood memories', expectedIndex: [49, 50, 59, 194], type: 'semantic', description: 'childhood → astronaut/spiders/grandma/Buddy' },
  { query: 'how I relax at night', expectedIndex: [10, 45, 73], type: 'semantic', description: 'relax night → read/journal/white noise' },
  { query: 'my favorite foods', expectedIndex: [52, 70, 59], type: 'semantic', description: 'fav food → Thai/burrito/pasta' },
  { query: 'technology I use daily', expectedIndex: [15, 26, 48, 84], type: 'semantic', description: 'tech daily → ThinkPad/Android/Notion/Jira' },
  { query: 'my weekend activities', expectedIndex: [4, 30, 44, 139, 150], type: 'semantic', description: 'weekend → soccer/food bank/FaceTime/woodwork/meal prep' },
  { query: 'my professional background', expectedIndex: [3, 19, 71, 127], type: 'semantic', description: 'professional → promoted/Microsoft/bootcamp/college' },
  { query: 'my guilty pleasures', expectedIndex: [70, 57], type: 'semantic', description: 'guilty pleasures → hot sauce / streaming' },
  { query: 'home office setup', expectedIndex: [15, 53, 196], type: 'semantic', description: 'home office → ThinkPad / standing desk / $400' },
  { query: 'future plans and goals', expectedIndex: [7, 25, 33, 58, 65, 174, 199], type: 'semantic', description: 'future → Italy/marathon/house/propose/Tesla/20 countries/YouTube' },
  { query: 'dietary supplements and health', expectedIndex: [64, 35, 43, 103], type: 'semantic', description: 'supplements → vitamins/fasting/vegetarian/melatonin' },
  { query: 'my coffee preferences', expectedIndex: [79, 146], type: 'semantic', description: 'coffee → flat white oat milk / Chemex' },
  { query: 'embarrassing moments', expectedIndex: [68, 157], type: 'semantic', description: 'embarrassing → failed driving / cry at movies' },
  { query: 'my charitable side', expectedIndex: [30, 51], type: 'semantic', description: 'charitable → food bank / Red Cross' },
  { query: 'movies and shows I love', expectedIndex: [41, 75], type: 'semantic', description: 'movies/shows → Breaking Bad / Shawshank' },
  { query: 'new skills I\'m developing', expectedIndex: [13, 47, 142], type: 'semantic', description: 'new skills → Spanish / guitar / chess' },
  { query: 'where do my relatives live', expectedIndex: [24, 44, 61, 101], type: 'semantic', description: 'relatives → Chicago/Seattle/Portland/Napa' },
  { query: 'my spicy food preference', expectedIndex: [52, 70], type: 'semantic', description: 'spicy → Thai / hot sauce burrito' },
  { query: 'DIY projects I\'ve done', expectedIndex: [39, 78, 139, 165], type: 'semantic', description: 'DIY → recipe app / treehouse / bookshelf / kitchen' },
  { query: 'things I\'m waiting for', expectedIndex: [72, 58, 65, 94], type: 'semantic', description: 'waiting → puppy/propose/Tesla/sister wedding' },
  { query: 'how I stay healthy', expectedIndex: [23, 25, 35, 42, 43, 60, 64], type: 'semantic', description: 'stay healthy → meditate/run/fast/gym/veg/5K/supps' },
  { query: 'my biggest regrets', expectedIndex: [12, 68, 167], type: 'semantic', description: 'regrets → crypto / driving test / SF condo loss' },
  { query: 'what scares me', expectedIndex: [6, 50, 77, 197], type: 'semantic', description: 'scares → heights/spiders/speaking/nightmare' },
  { query: 'building things with my hands', expectedIndex: [59, 78, 139], type: 'semantic', description: 'hands → pasta / treehouse / bookshelf' },
  { query: 'my productivity tools', expectedIndex: [48, 15, 53, 84], type: 'semantic', description: 'productivity → Notion/ThinkPad/standing desk/Jira' },
  { query: 'my noise sensitivity', expectedIndex: [56, 73, 191], type: 'semantic', description: 'noise → neighbor dog / white noise / chewing' },
  { query: 'who am I mentoring or coaching', expectedIndex: [37, 66, 134], type: 'semantic', description: 'mentor/coach → juniors / daughter team / TA' },
  { query: 'how much do I spend monthly', expectedIndex: [22, 46, 57, 114], type: 'semantic', description: 'monthly spend → mortgage/insurance/streaming/car loan' },
  { query: 'things I do for fun on weekdays', expectedIndex: [16, 47, 142, 172], type: 'semantic', description: 'weekday fun → basketball / guitar / chess / dance' },
  { query: 'my plant-based lifestyle', expectedIndex: [40, 43, 79], type: 'semantic', description: 'plant-based → oat milk/vegetarian/flat white' },
  { query: 'my life insurance and safety', expectedIndex: [46, 62, 113], type: 'semantic', description: 'insurance/safety → Geico / EpiPen / life insurance' },
  { query: 'food that made me sick', expectedIndex: 74, type: 'semantic', description: 'sick food → sushi food poisoning' },
  { query: 'my art and creative pursuits', expectedIndex: [47, 39, 140, 199], type: 'semantic', description: 'creative → guitar / recipe app / photography / YouTube' },
  { query: 'things about my physical appearance', expectedIndex: [67, 169, 185, 189], type: 'semantic', description: 'appearance → tattoo/gray hair/height/birthmark' },
  { query: 'my retirement planning', expectedIndex: [76, 111, 116], type: 'semantic', description: 'retirement → 401k/index funds/Roth IRA' },

  // New semantic queries targeting memories 80-199
  { query: 'my work projects and achievements', expectedIndex: [80, 83, 90, 170], type: 'semantic', description: 'work achievements → Aurora/review/bonus/patent' },
  { query: 'my parents and their careers', expectedIndex: [92, 93], type: 'semantic', description: 'parents → dad teacher / mom nurse' },
  { query: 'upcoming family celebrations', expectedIndex: [94, 95, 198], type: 'semantic', description: 'family events → sister wedding / Thanksgiving / Christmas' },
  { query: 'my children and their lives', expectedIndex: [4, 20, 96, 100], type: 'semantic', description: 'children → son soccer/daughter bday/3rd grade/vet dream' },
  { query: 'who my wife is', expectedIndex: [14, 97, 168, 172], type: 'semantic', description: 'wife → dating app/designer/eloped/dance' },
  { query: 'extended family members', expectedIndex: [98, 101], type: 'semantic', description: 'extended family → father-in-law colonel / uncle vineyard' },
  { query: 'my breathing problems', expectedIndex: 102, type: 'semantic', description: 'breathing → asthma inhaler' },
  { query: 'things I take as medicine or supplements', expectedIndex: [64, 103, 106], type: 'semantic', description: 'medicine → vitamins/melatonin/contacts' },
  { query: 'doctor appointments coming up', expectedIndex: [104, 107, 108], type: 'semantic', description: 'appointments → cholesterol/chiropractor/dental' },
  { query: 'head injuries I have had', expectedIndex: 110, type: 'semantic', description: 'head injury → concussion football' },
  { query: 'my investment portfolio', expectedIndex: [111, 116], type: 'semantic', description: 'portfolio → 70% index funds / Roth IRA' },
  { query: 'how much money I make', expectedIndex: [112, 90], type: 'semantic', description: 'income → $165k salary / $15k bonus' },
  { query: 'insurance coverage I have', expectedIndex: [46, 113], type: 'semantic', description: 'insurance → Geico car / Northwestern Mutual life' },
  { query: 'debts I owe', expectedIndex: [22, 114], type: 'semantic', description: 'debts → mortgage / car loan' },
  { query: 'tax and financial planning', expectedIndex: [76, 115, 116, 118], type: 'semantic', description: 'tax/finance → 401k/TurboTax/Roth/emergency fund' },
  { query: 'my creditworthiness', expectedIndex: 117, type: 'semantic', description: 'credit → 780 score' },
  { query: 'regular social gatherings', expectedIndex: [119, 123, 125, 173], type: 'semantic', description: 'gatherings → poker/BBQ/game night/book club' },
  { query: 'romantic things I did for my wife', expectedIndex: [120, 168, 172], type: 'semantic', description: 'romantic → surprise party / eloped / dance class' },
  { query: 'friends who live abroad', expectedIndex: [34, 121], type: 'semantic', description: 'abroad friends → Dave London / Mike Japan' },
  { query: 'my college experience', expectedIndex: [127, 128, 129, 130, 131, 133], type: 'semantic', description: 'college → UMich/Dr.Chen/orgo/hackathon/thesis/Berlin' },
  { query: 'academic achievements', expectedIndex: [130, 131, 132, 134], type: 'semantic', description: 'academic → hackathon/thesis/scholarship/TA' },
  { query: 'time I spent in Germany', expectedIndex: [133, 193], type: 'semantic', description: 'Germany → Berlin study abroad / French roommates' },
  { query: 'creative hobbies and crafts', expectedIndex: [135, 136, 138, 139, 140, 183], type: 'semantic', description: 'crafts → puzzle/brew/vinyl/woodwork/photo/sourdough' },
  { query: 'my running history and times', expectedIndex: [25, 60, 137], type: 'semantic', description: 'running → half marathon / 5K / 1:52' },
  { query: 'my collection hobbies', expectedIndex: [138, 135], type: 'semantic', description: 'collections → vinyl records / puzzles' },
  { query: 'what I grow at home', expectedIndex: [141, 183], type: 'semantic', description: 'grow → garden vegetables / sourdough starter' },
  { query: 'games I play', expectedIndex: [142, 119, 159], type: 'semantic', description: 'games → chess / poker / competitive board games' },
  { query: 'my commute details', expectedIndex: [32, 143, 149], type: 'semantic', description: 'commute → train 45min / 7:15 Hoboken / podcasts' },
  { query: 'what I eat during the work day', expectedIndex: [144, 146], type: 'semantic', description: 'work food → Sweetgreen salad / Chemex coffee' },
  { query: 'evening routine with family', expectedIndex: [147, 148], type: 'semantic', description: 'evening → home 7pm / walk cats 8pm' },
  { query: 'how I prepare meals for the week', expectedIndex: [144, 150], type: 'semantic', description: 'meal planning → Sweetgreen / Sunday prep' },
  { query: 'my personality weaknesses', expectedIndex: [151, 155, 158], type: 'semantic', description: 'weaknesses → overthink / road rage / procrastinate' },
  { query: 'how I behave in social settings', expectedIndex: [152, 159, 180], type: 'semantic', description: 'social → introvert / competitive / deep conversation' },
  { query: 'my sense of punctuality', expectedIndex: 153, type: 'semantic', description: 'punctuality → 10 min early' },
  { query: 'when I am most productive', expectedIndex: [42, 154], type: 'semantic', description: 'productive → morning person / gym 5:30' },
  { query: 'my emotional side', expectedIndex: [157, 186, 197], type: 'semantic', description: 'emotional → cry movies / anxiety / nightmares' },
  { query: 'places I have lived', expectedIndex: [160, 176, 167], type: 'semantic', description: 'lived → SF / Hoboken NJ / sold condo' },
  { query: 'why I chose Microsoft', expectedIndex: [161, 166], type: 'semantic', description: 'chose MSFT → work-life balance / turned down Google' },
  { query: 'stories about my cats', expectedIndex: [27, 148, 162], type: 'semantic', description: 'cat stories → Luna Mochi / walk / shelter stray' },
  { query: 'car related events', expectedIndex: [2, 46, 114, 163], type: 'semantic', description: 'car → BMW / Geico / loan / accident' },
  { query: 'my best trips abroad', expectedIndex: [36, 133, 164], type: 'semantic', description: 'abroad trips → Bali / Berlin / Tokyo' },
  { query: 'home renovation and improvements', expectedIndex: [165, 178, 196], type: 'semantic', description: 'home improve → kitchen $25k / solar / standing desk' },
  { query: 'job offers I received', expectedIndex: [19, 166], type: 'semantic', description: 'job offers → Microsoft / Google turned down' },
  { query: 'money I have lost', expectedIndex: [12, 167], type: 'semantic', description: 'lost money → crypto $5k / condo $30k' },
  { query: 'how my wedding happened', expectedIndex: 168, type: 'semantic', description: 'wedding → eloped Vegas then proper' },
  { query: 'signs of aging', expectedIndex: [106, 169], type: 'semantic', description: 'aging → gray hair 28 / contacts prescription' },
  { query: 'intellectual property I own', expectedIndex: 170, type: 'semantic', description: 'IP → patent caching algorithm' },
  { query: 'job interviews that went badly', expectedIndex: 171, type: 'semantic', description: 'bad interview → Meta system design' },
  { query: 'date night activities', expectedIndex: 172, type: 'semantic', description: 'date night → salsa dance Thursday' },
  { query: 'my reading habits', expectedIndex: [10, 17, 173, 182], type: 'semantic', description: 'reading → before bed / Sapiens / book club / paper books' },
  { query: 'my travel bucket list', expectedIndex: [7, 174], type: 'semantic', description: 'travel goals → Italy / 20 countries by 40' },
  { query: 'travel documents', expectedIndex: 175, type: 'semantic', description: 'documents → passport 2036' },
  { query: 'details about my house', expectedIndex: [176, 177, 165], type: 'semantic', description: 'house → 3BR Hoboken / backyard / kitchen reno' },
  { query: 'outdoor spaces at my house', expectedIndex: [141, 177], type: 'semantic', description: 'outdoor → garden / backyard grill fire pit' },
  { query: 'green energy interest', expectedIndex: [65, 178], type: 'semantic', description: 'green → Tesla / solar panels' },
  { query: 'my travel preferences', expectedIndex: 179, type: 'semantic', description: 'travel pref → window seat' },
  { query: 'how I like to communicate', expectedIndex: [152, 180], type: 'semantic', description: 'communication → introvert / hate small talk' },
  { query: 'my sleeping preferences', expectedIndex: [73, 103, 181], type: 'semantic', description: 'sleep pref → white noise / melatonin / left side' },
  { query: 'my baking projects', expectedIndex: [59, 183], type: 'semantic', description: 'baking → grandma pasta / Bready Mercury sourdough' },
  { query: 'my body measurements', expectedIndex: [184, 185], type: 'semantic', description: 'body → shoe 10.5 / 5\'11 175lbs' },
  { query: 'my mental health', expectedIndex: [151, 186, 197], type: 'semantic', description: 'mental health → overthink / anxiety / nightmares' },
  { query: 'my vision and eyesight', expectedIndex: [106, 187], type: 'semantic', description: 'vision → contacts -3.5 / reading glasses' },
  { query: 'physical traits that make me unique', expectedIndex: [67, 189, 190], type: 'semantic', description: 'unique traits → tattoo / birthmark / left-handed' },
  { query: 'sound sensitivities', expectedIndex: [56, 73, 191], type: 'semantic', description: 'sound → neighbor dog / white noise / chewing' },
  { query: 'languages I speak', expectedIndex: [13, 193], type: 'semantic', description: 'languages → Spanish A2 / French conversational' },
  { query: 'pets I have had in my life', expectedIndex: [27, 72, 162, 194], type: 'semantic', description: 'lifetime pets → cats / puppy / adoption / Buddy' },
  { query: 'my birth order and siblings', expectedIndex: [44, 61, 94, 195], type: 'semantic', description: 'siblings → sister Seattle / brother Portland / Emma wedding / middle child' },
  { query: 'my recurring dreams', expectedIndex: 197, type: 'semantic', description: 'dreams → chased dark forest' },
  { query: 'holidays and traditions', expectedIndex: [51, 95, 123, 198], type: 'semantic', description: 'holidays → Red Cross Xmas / Thanksgiving / BBQ July 4 / Christmas' },
  { query: 'content creation ideas', expectedIndex: [39, 199], type: 'semantic', description: 'content → recipe app / YouTube cooking' },

  // Additional semantic queries
  { query: 'my office culture', expectedIndex: [82, 84, 85, 91], type: 'semantic', description: 'office culture → Sarah donuts / Jira / Tom / standups' },
  { query: 'my in-laws', expectedIndex: 98, type: 'semantic', description: 'in-laws → father-in-law Army colonel' },
  { query: 'dental and oral health', expectedIndex: [61, 105, 108], type: 'semantic', description: 'dental → brother dentist / wisdom teeth / cleaning' },
  { query: 'my eyesight problems', expectedIndex: [106, 187], type: 'semantic', description: 'eyesight → contacts -3.5 / reading glasses' },
  { query: 'how I handle money', expectedIndex: [111, 115, 117, 118], type: 'semantic', description: 'money mgmt → index funds / TurboTax / credit 780 / emergency fund' },
  { query: 'my Hoboken neighborhood', expectedIndex: [123, 143, 176, 177], type: 'semantic', description: 'Hoboken → BBQ / train station / 3BR / backyard' },
  { query: 'things I learned from family members', expectedIndex: [59, 92, 93], type: 'semantic', description: 'family lessons → grandma pasta / dad teacher / mom nurse' },
  { query: 'my professional network', expectedIndex: [8, 82, 85, 121, 166], type: 'semantic', description: 'network → Kevin Google / Sarah / Tom / Mike / Google offer' },
  { query: 'competitions I have entered', expectedIndex: [130, 137, 140, 142], type: 'semantic', description: 'competitions → hackathon / half marathon / photo contest / chess' },
  { query: 'things I do on my own time', expectedIndex: [10, 17, 23, 45, 135, 142], type: 'semantic', description: 'alone time → read / Sapiens / meditate / journal / puzzle / chess' },
  { query: 'beverages I enjoy', expectedIndex: [5, 40, 79, 136, 146], type: 'semantic', description: 'beverages → quit drinking / oat milk / flat white / brew beer / Chemex' },
  { query: 'what I eat for breakfast', expectedIndex: [35, 43, 146], type: 'semantic', description: 'breakfast → IF skip / vegetarian / coffee Chemex' },
  { query: 'my professional development', expectedIndex: [11, 37, 71, 131, 170], type: 'semantic', description: 'prof dev → MBA / mentoring / bootcamp / thesis / patent' },
  { query: 'sensory things that bother me', expectedIndex: [6, 50, 56, 191], type: 'semantic', description: 'sensory → heights / spiders / dog bark / chewing sound' },
  { query: 'gifts my family might like', expectedIndex: [63, 97, 100, 138], type: 'semantic', description: 'family gifts → Radiohead vinyl / wife designer / daughter vet / vinyl records' },
  { query: 'my Microsoft colleagues', expectedIndex: [31, 37, 82, 85], type: 'semantic', description: 'colleagues → team 8 / juniors / Sarah / Tom' },
  { query: 'things I built or created', expectedIndex: [39, 78, 131, 136, 139, 170, 183], type: 'semantic', description: 'created → recipe app / treehouse / thesis / beer / bookshelf / patent / sourdough' },
  { query: 'my real estate history', expectedIndex: [22, 33, 165, 167, 176], type: 'semantic', description: 'real estate → mortgage / buy house / kitchen reno / sold condo / 3BR' },
  { query: 'things related to Italy', expectedIndex: [7, 28, 59], type: 'semantic', description: 'Italy → trip June / Italian restaurant / grandma pasta' },
  { query: 'my San Francisco memories', expectedIndex: [160, 161, 167], type: 'semantic', description: 'SF → moved from / startup / sold condo' },
  { query: 'how I spend Saturday', expectedIndex: [4, 139, 145], type: 'semantic', description: 'Saturday → son soccer / woodwork / pickup 5pm' },
  { query: 'my approach to cooking and food prep', expectedIndex: [59, 141, 144, 150, 183], type: 'semantic', description: 'food prep → pasta / garden / Sweetgreen / meal prep / sourdough' },
  { query: 'activities I do with my wife', expectedIndex: [120, 168, 172], type: 'semantic', description: 'with wife → surprise party / Vegas / salsa dance' },
  { query: 'my tech career path', expectedIndex: [3, 19, 71, 80, 127, 161, 170, 171], type: 'semantic', description: 'tech career → promoted/Microsoft/bootcamp/Aurora/UMich/startup/patent/Meta' },
  { query: 'things I spend money on for fun', expectedIndex: [47, 57, 136, 138, 139], type: 'semantic', description: 'fun spending → guitar / streaming / brew / vinyl / woodwork' },
  { query: 'health checkups and preventive care', expectedIndex: [64, 104, 107, 108, 109], type: 'semantic', description: 'preventive → supplements / cholesterol / chiro / dental / heart rate' },
  { query: 'my neighborhood and community', expectedIndex: [30, 51, 56, 123, 176], type: 'semantic', description: 'community → food bank / Red Cross / neighbor / BBQ / Hoboken' },
  { query: 'skills I have practiced a long time', expectedIndex: [21, 59, 136, 142], type: 'semantic', description: 'practiced → Python / pasta / brew beer / chess' },
  { query: 'memorable parties and celebrations', expectedIndex: [95, 99, 120, 125, 168], type: 'semantic', description: 'parties → Thanksgiving / anniversary / surprise party / game night / Vegas' },
  { query: 'outdoor activities I enjoy', expectedIndex: [25, 60, 141, 177], type: 'semantic', description: 'outdoor → half marathon / 5K / garden / backyard BBQ' },

  // ══════════════════════════════════════════════════════════════
  // ── Hard queries (100) — negation/aggregation/cross-domain/temporal/abstract
  // ══════════════════════════════════════════════════════════════

  // Negation queries
  { query: 'what foods can I not eat', expectedIndex: [1, 43, 62], type: 'hard', description: 'NEG: can\'t eat → shellfish/vegetarian/peanut' },
  { query: 'activities I avoid because of fear', expectedIndex: [6, 77], type: 'hard', description: 'NEG: avoid → heights / public speaking' },
  { query: 'things I stopped doing', expectedIndex: 5, type: 'hard', description: 'NEG: stopped → quit drinking' },
  { query: 'things I don\'t like', expectedIndex: [50, 56, 180, 191], type: 'hard', description: 'NEG: dislike → spiders/dog barking/small talk/chewing' },
  { query: 'what technology did I give up', expectedIndex: 26, type: 'hard', description: 'NEG: gave up → iPhone' },
  { query: 'job offers I rejected', expectedIndex: 166, type: 'hard', description: 'NEG: rejected → Google offer' },
  { query: 'tests or exams I didn\'t pass', expectedIndex: [68, 129, 171], type: 'hard', description: 'NEG: didn\'t pass → driving/orgo chem/Meta' },
  { query: 'what am I not good at', expectedIndex: [77, 151, 155, 158], type: 'hard', description: 'NEG: not good at → speaking/overthink/road rage/procrastinate' },
  { query: 'things that keep me up at night', expectedIndex: [56, 186, 197], type: 'hard', description: 'NEG: sleep problems → dog/anxiety/nightmares' },
  { query: 'what I would never order at a restaurant', expectedIndex: [1, 62, 74], type: 'hard', description: 'NEG: never order → shellfish/peanut/sushi' },

  // Aggregation queries
  { query: 'describe my typical weekday from morning to night', expectedIndex: [0, 23, 42, 60, 91, 143, 144, 147, 148], type: 'hard', description: 'AGG: full day → wake/meditate/gym/run/standup/train/lunch/home/cats' },
  { query: 'list all my family members', expectedIndex: [24, 44, 61, 92, 93, 94, 97, 98, 195], type: 'hard', description: 'AGG: all family → mom/sister/brother/dad/mom nurse/Emma/wife/FIL/middle' },
  { query: 'summarize my financial situation', expectedIndex: [22, 76, 111, 112, 114, 117, 118], type: 'hard', description: 'AGG: finances → mortgage/401k/index/salary/car loan/credit/emergency' },
  { query: 'all the sports and physical activities I do', expectedIndex: [16, 25, 42, 60, 137, 172], type: 'hard', description: 'AGG: sports → basketball/marathon/gym/5K/half marathon/salsa' },
  { query: 'everyone I know by name', expectedIndex: [8, 34, 82, 85, 121, 124, 128], type: 'hard', description: 'AGG: names → Kevin/Dave/Sarah/Tom/Mike/Lisa/Dr.Chen' },
  { query: 'everything wrong with my health', expectedIndex: [1, 18, 29, 55, 62, 102, 106, 110, 186], type: 'hard', description: 'AGG: health issues → allergy/knee/back/arm/peanut/asthma/eyes/concussion/anxiety' },
  { query: 'all the places I have been', expectedIndex: [36, 122, 133, 160, 164, 174], type: 'hard', description: 'AGG: places → Bali/London/Berlin/SF/Tokyo/14 countries' },
  { query: 'how much money do I spend each month total', expectedIndex: [22, 46, 57, 113, 114], type: 'hard', description: 'AGG: monthly total → mortgage/car ins/streaming/life ins/car loan' },
  { query: 'all my creative hobbies and outlets', expectedIndex: [39, 47, 136, 138, 139, 140, 183, 199], type: 'hard', description: 'AGG: creative → recipe app/guitar/brew/vinyl/woodwork/photo/sourdough/YouTube' },
  { query: 'every educational experience I\'ve had', expectedIndex: [11, 71, 127, 128, 129, 130, 131, 133, 134], type: 'hard', description: 'AGG: education → MBA/bootcamp/UMich/professor/orgo/hackathon/thesis/Berlin/TA' },

  // Cross-domain queries
  { query: 'how does my work schedule affect family time', expectedIndex: [32, 91, 143, 147, 148], type: 'hard', description: 'CROSS: work↔family → commute/standup/train/home 7pm/cats 8pm' },
  { query: 'what does my diet say about my values', expectedIndex: [40, 43, 79], type: 'hard', description: 'CROSS: diet↔values → oat milk/vegetarian/plant-based' },
  { query: 'how my childhood influences my parenting', expectedIndex: [49, 66, 78, 100], type: 'hard', description: 'CROSS: childhood↔parent → astronaut/coaching/treehouse/daughter vet' },
  { query: 'connections between my hobbies and career', expectedIndex: [21, 39, 47, 80, 81], type: 'hard', description: 'CROSS: hobby↔career → Python/recipe app/guitar/Aurora/tech stack' },
  { query: 'how exercise affects my health conditions', expectedIndex: [18, 25, 29, 42, 60, 109], type: 'hard', description: 'CROSS: exercise↔health → knee/marathon/back/gym/5K/heart rate' },
  { query: 'how my finances relate to life goals', expectedIndex: [33, 65, 76, 111, 118], type: 'hard', description: 'CROSS: finance↔goals → house/Tesla/401k/index/emergency' },
  { query: 'how my college experience shaped my career', expectedIndex: [19, 71, 127, 130, 131], type: 'hard', description: 'CROSS: college↔career → Microsoft/bootcamp/UMich/hackathon/thesis' },
  { query: 'how my social life interacts with being an introvert', expectedIndex: [119, 125, 152, 159, 180], type: 'hard', description: 'CROSS: social↔introvert → poker/game night/introvert/competitive/small talk' },
  { query: 'how my allergies affect my dining choices', expectedIndex: [1, 28, 52, 62, 74], type: 'hard', description: 'CROSS: allergy↔dining → shellfish/Italian/Thai/peanut/sushi' },
  { query: 'my work-life balance strategy', expectedIndex: [32, 42, 88, 147, 161], type: 'hard', description: 'CROSS: work-life → commute/gym/PTO/home 7pm/left startup' },

  // Temporal reasoning queries
  { query: 'what did I change in the last year', expectedIndex: [3, 5, 26, 47, 65], type: 'hard', description: 'TEMP: last year → promoted/quit drinking/Android/guitar/saving Tesla' },
  { query: 'what appointments do I have coming up', expectedIndex: [87, 107, 108], type: 'hard', description: 'TEMP: upcoming → offsite Austin / chiropractor / dental' },
  { query: 'things I did in college years ago', expectedIndex: [55, 71, 127, 128, 129, 130, 131, 133, 134], type: 'hard', description: 'TEMP: college era → football/bootcamp/UMich/professor/orgo/hackathon/thesis/Berlin/TA' },
  { query: 'habits I developed in the last few months', expectedIndex: [23, 25, 35, 45, 47], type: 'hard', description: 'TEMP: recent habits → meditate/marathon/fasting/journal/guitar' },
  { query: 'what I did as a teenager', expectedIndex: [49, 50, 68, 110], type: 'hard', description: 'TEMP: teenage → astronaut dream/spiders/driving test/concussion' },
  { query: 'upcoming events in my calendar', expectedIndex: [7, 58, 87, 94, 108], type: 'hard', description: 'TEMP: calendar → Italy June/propose Sept/offsite/sister Oct/dental Tue' },
  { query: 'my life before Microsoft', expectedIndex: [71, 127, 133, 160, 161, 167], type: 'hard', description: 'TEMP: before MSFT → bootcamp/college/Berlin/SF/left startup/sold condo' },
  { query: 'things that happened to me in the past month', expectedIndex: [74, 121, 125, 135, 139], type: 'hard', description: 'TEMP: past month → food poisoning/Mike returned/game night/puzzle/bookshelf' },
  { query: 'childhood pets versus current pets', expectedIndex: [27, 72, 162, 194], type: 'hard', description: 'TEMP: pets timeline → Buddy then / Luna Mochi now / puppy soon' },
  { query: 'how has my career progressed over time', expectedIndex: [3, 19, 71, 80, 83, 127, 161, 170], type: 'hard', description: 'TEMP: career arc → college/bootcamp/startup/Microsoft/promoted/Aurora/review/patent' },

  // Abstract reasoning queries
  { query: 'what kind of person am I', expectedIndex: [151, 152, 153, 154, 156, 159, 190], type: 'hard', description: 'ABS: personality → overthink/introvert/punctual/morning/organized/competitive/left-handed' },
  { query: 'how would you describe my taste', expectedIndex: [28, 41, 52, 63, 75, 79, 188], type: 'hard', description: 'ABS: taste → Italian rest/BB/Thai/Radiohead/Shawshank/coffee/navy blue' },
  { query: 'what does my daily schedule reveal about me', expectedIndex: [0, 23, 42, 91, 143, 154], type: 'hard', description: 'ABS: schedule → early riser/meditate/gym/standup/train/morning person' },
  { query: 'how risk-tolerant am I financially', expectedIndex: [12, 76, 111, 118], type: 'hard', description: 'ABS: risk → lost crypto / maxed 401k / index funds / emergency fund' },
  { query: 'what motivates me in life', expectedIndex: [3, 25, 37, 49, 174], type: 'hard', description: 'ABS: motivation → promoted/marathon/mentoring/astronaut dream/travel 20 countries' },
  { query: 'how important is family to me', expectedIndex: [4, 20, 44, 66, 78, 95, 198], type: 'hard', description: 'ABS: family importance → son soccer/daughter bday/sister/coach/treehouse/Thanksgiving/Christmas' },
  { query: 'what are my sources of stress', expectedIndex: [29, 56, 77, 151, 155, 186], type: 'hard', description: 'ABS: stress → back pain/dog barking/public speaking/overthink/road rage/anxiety' },
  { query: 'am I a creature of habit', expectedIndex: [0, 23, 35, 42, 45, 64, 150, 153], type: 'hard', description: 'ABS: habits → wake 6/meditate/fast/gym/journal/supps/meal prep/punctual' },
  { query: 'how environmentally conscious am I', expectedIndex: [40, 43, 65, 178], type: 'hard', description: 'ABS: eco → oat milk/vegetarian/Tesla/solar panels' },
  { query: 'how much of a foodie am I', expectedIndex: [28, 52, 59, 70, 136, 141, 183], type: 'hard', description: 'ABS: foodie → Italian rest/Thai/pasta/hot sauce/brew beer/garden/sourdough' },

  // More abstract/hard
  { query: 'contradictions in my personality', expectedIndex: [152, 159, 158], type: 'hard', description: 'ABS: contradictions → introvert but competitive / procrastinate chores not work' },
  { query: 'what would I need in a medical emergency', expectedIndex: [9, 62, 102], type: 'hard', description: 'ABS: emergency medical → blood type A+ / EpiPen / inhaler' },
  { query: 'things my kids can learn from me', expectedIndex: [16, 25, 47, 59, 139, 142], type: 'hard', description: 'ABS: teach kids → basketball/running/guitar/pasta/woodwork/chess' },
  { query: 'how has my identity evolved', expectedIndex: [3, 5, 26, 43, 160, 161, 169], type: 'hard', description: 'ABS: identity → promoted/sober/Android/vegetarian/moved/changed jobs/gray hair' },
  { query: 'skills I could monetize', expectedIndex: [21, 39, 136, 139, 140, 170, 199], type: 'hard', description: 'ABS: monetize → Python/recipe app/brew/woodwork/photo/patent/YouTube' },
  { query: 'what makes me vulnerable', expectedIndex: [6, 50, 62, 77, 151, 186], type: 'hard', description: 'ABS: vulnerable → heights/spiders/peanut/speaking/overthink/anxiety' },
  { query: 'things I do alone vs with others', expectedIndex: [10, 23, 45, 119, 125, 142, 173], type: 'hard', description: 'ABS: alone vs social → read/meditate/journal/poker/game night/chess/book club' },
  { query: 'how prepared am I for emergencies', expectedIndex: [62, 102, 113, 118], type: 'hard', description: 'ABS: prepared → EpiPen/inhaler/life insurance/emergency fund' },
  { query: 'what would a stranger notice about me first', expectedIndex: [67, 185, 190], type: 'hard', description: 'ABS: first impression → tattoo/height 5\'11/left-handed' },
  { query: 'my relationship with technology', expectedIndex: [15, 26, 48, 54, 81, 84], type: 'hard', description: 'ABS: tech relationship → ThinkPad/Android/Notion/screen time/tech stack/Jira' },

  // More hard cross-domain
  { query: 'what would I pack for the Italy trip', expectedIndex: [7, 62, 102, 106, 175, 179], type: 'hard', description: 'CROSS: Italy packing → trip/EpiPen/inhaler/contacts/passport/window seat' },
  { query: 'how my health limits what I can do', expectedIndex: [1, 18, 29, 62, 102], type: 'hard', description: 'CROSS: health limits → shellfish/knee/back/peanut/asthma' },
  { query: 'my total annual compensation and benefits', expectedIndex: [88, 90, 112, 113], type: 'hard', description: 'CROSS: total comp → PTO/bonus/salary/life insurance' },
  { query: 'how my hobbies connect to people in my life', expectedIndex: [47, 63, 119, 124, 138, 172, 173], type: 'hard', description: 'CROSS: hobbies↔people → guitar/Radiohead/poker/Lisa wine/vinyl/dance/book club' },
  { query: 'things that would break my routine', expectedIndex: [7, 87, 94, 108], type: 'hard', description: 'CROSS: routine break → Italy trip/Austin offsite/sister wedding/dental' },
  { query: 'how my past failures made me who I am', expectedIndex: [12, 68, 129, 161, 167, 171], type: 'hard', description: 'CROSS: failure→growth → crypto/driving/orgo/changed jobs/condo loss/Meta' },
  { query: 'what I value most based on how I spend time', expectedIndex: [4, 23, 25, 30, 37, 45], type: 'hard', description: 'ABS: values → son soccer/meditate/marathon/food bank/mentoring/journal' },
  { query: 'my New Jersey life versus San Francisco life', expectedIndex: [19, 160, 161, 167, 176], type: 'hard', description: 'CROSS: NJ vs SF → Microsoft/moved/work-life/sold condo/Hoboken' },
  { query: 'what keeps my marriage strong', expectedIndex: [44, 97, 120, 168, 172], type: 'hard', description: 'CROSS: marriage → FaceTime sister(family)/wife designer/surprise party/eloped/dance' },
  { query: 'how I would describe myself on a dating profile', expectedIndex: [43, 47, 152, 154, 190, 192], type: 'hard', description: 'ABS: dating profile → vegetarian/guitar/introvert/morning person/left-handed/birthday' },

  // Additional hard queries
  { query: 'what makes me a good father', expectedIndex: [4, 66, 78, 96, 100, 145], type: 'hard', description: 'ABS: good dad → son soccer/coached/treehouse/school/vet dream/pickup' },
  { query: 'how would my coworkers describe me', expectedIndex: [3, 37, 83, 86, 153, 156, 170], type: 'hard', description: 'ABS: coworker view → promoted/mentor/review/presented/punctual/organized/patent' },
  { query: 'what I would need if I moved abroad', expectedIndex: [13, 62, 102, 175, 193], type: 'hard', description: 'CROSS: move abroad → Spanish/EpiPen/inhaler/passport/French' },
  { query: 'why am I not sleeping well', expectedIndex: [29, 56, 73, 103, 186, 197], type: 'hard', description: 'CROSS: sleep issues → back pain/dog bark/white noise/melatonin/anxiety/nightmares' },
  { query: 'things that could trigger an allergic reaction at dinner', expectedIndex: [1, 62, 74], type: 'hard', description: 'CROSS: allergy danger → shellfish/peanut/sushi' },
  { query: 'how I balance being introverted with social obligations', expectedIndex: [30, 119, 125, 152, 173, 180], type: 'hard', description: 'ABS: introvert balance → food bank/poker/game night/introvert/book club/small talk' },
  { query: 'what my house says about my personality', expectedIndex: [53, 141, 156, 176, 177, 196], type: 'hard', description: 'ABS: house↔personality → desk/garden/organized/3BR/backyard/desk converter' },
  { query: 'evidence that I value education', expectedIndex: [11, 37, 71, 96, 100, 127, 131, 132, 134], type: 'hard', description: 'ABS: education value → MBA/mentor/bootcamp/son school/daughter vet/UMich/thesis/scholarship/TA' },
  { query: 'all the things connected to my back pain', expectedIndex: [18, 29, 53, 107, 196], type: 'hard', description: 'CROSS: back pain ecosystem → knee surgery/back pain/standing desk/chiropractor/desk converter' },
  { query: 'how my eating changed over time', expectedIndex: [5, 35, 40, 43, 150], type: 'hard', description: 'TEMP: eating evolution → quit drinking/IF/oat milk/vegetarian 3yr/meal prep' },
  { query: 'what a personal trainer should know about me', expectedIndex: [18, 25, 29, 42, 55, 60, 109, 110, 137, 185], type: 'hard', description: 'CROSS: trainer info → knee/marathon/back/gym/arm/5K/heart rate/concussion/time/weight' },
  { query: 'if I had to describe my life in 5 facts', expectedIndex: [19, 27, 97, 152, 176], type: 'hard', description: 'ABS: 5 facts → Microsoft/cats/wife/introvert/Hoboken' },
  { query: 'things my doctor needs to know', expectedIndex: [1, 9, 18, 29, 55, 62, 64, 102, 103, 110], type: 'hard', description: 'ABS: doctor info → shellfish/blood/knee/back/arm/peanut/supps/asthma/melatonin/concussion' },
  { query: 'what I have in common with my college friends', expectedIndex: [8, 16, 119, 121, 126, 127], type: 'hard', description: 'CROSS: college friends → Kevin/basketball/poker/Mike/group chat/UMich' },
  { query: 'how my hobbies have evolved from childhood', expectedIndex: [47, 49, 55, 136, 138, 139, 142, 194], type: 'hard', description: 'TEMP: hobby evolution → guitar/astronaut/football/brew/vinyl/woodwork/chess/dog' },
  { query: 'reasons I might need to leave work early', expectedIndex: [96, 100, 108, 145], type: 'hard', description: 'CROSS: leave early → son school/daughter/dental/pickup soccer' },
  { query: 'what I would put on my resume', expectedIndex: [3, 19, 80, 83, 90, 127, 131, 170], type: 'hard', description: 'ABS: resume → promoted/Microsoft/Aurora/review/bonus/UMich/thesis/patent' },
  { query: 'clues about my political values', expectedIndex: [40, 43, 65, 178], type: 'hard', description: 'ABS: values → oat milk/vegetarian/Tesla/solar panels' },
  { query: 'how would I furnish a new home', expectedIndex: [53, 73, 138, 177, 182, 196], type: 'hard', description: 'ABS: furnish → standing desk/white noise/vinyl shelf/backyard/bookshelves/desk converter' },
  { query: 'what keeps me grounded', expectedIndex: [4, 23, 30, 44, 45, 51], type: 'hard', description: 'ABS: grounded → son soccer/meditate/food bank/sister/journal/Red Cross' },
  { query: 'tensions between my goals and reality', expectedIndex: [11, 25, 29, 33, 65, 186], type: 'hard', description: 'ABS: tension → MBA/marathon/back pain/buy house/Tesla/anxiety' },
  { query: 'what would I talk about on a first date', expectedIndex: [7, 36, 47, 63, 164, 174], type: 'hard', description: 'ABS: first date → Italy trip/Bali/guitar/Radiohead/Tokyo/travel goal' },
  { query: 'everything connected to food in my life', expectedIndex: [1, 28, 43, 52, 59, 62, 70, 74, 136, 141, 144, 150, 183], type: 'hard', description: 'AGG: all food → allergy/Italian/vegetarian/Thai/pasta/peanut/burrito/sushi/brew/garden/lunch/prep/sourdough' },
  { query: 'all recurring weekly commitments', expectedIndex: [4, 16, 30, 44, 60, 107, 119, 172, 173], type: 'hard', description: 'AGG: weekly → son soccer/basketball/food bank/FaceTime/5K/chiro/poker/dance/book club' },
  { query: 'how my mental health affects daily life', expectedIndex: [45, 73, 103, 151, 155, 186, 197], type: 'hard', description: 'CROSS: mental↔daily → journal/white noise/melatonin/overthink/road rage/anxiety/nightmares' },
  { query: 'differences between my work self and home self', expectedIndex: [19, 53, 139, 148, 153, 156, 158], type: 'hard', description: 'ABS: work vs home → Microsoft/desk/woodwork/cats/punctual/organized/procrastinate chores' },
  { query: 'what my spending reveals about priorities', expectedIndex: [22, 57, 65, 76, 111, 132, 165], type: 'hard', description: 'ABS: spending → mortgage/streaming/Tesla/401k/index funds/scholarship/kitchen $25k' },
  { query: 'all the medical professionals I see', expectedIndex: [61, 104, 107, 108], type: 'hard', description: 'AGG: doctors → brother dentist / cholesterol doc / chiropractor / dental cleaning' },
  { query: 'how I would survive a zombie apocalypse', expectedIndex: [25, 42, 60, 62, 102, 118, 139, 141], type: 'hard', description: 'ABS: survival → marathon/gym/5K/EpiPen/inhaler/emergency fund/woodwork/garden' },
  { query: 'everything that makes my mornings chaotic', expectedIndex: [0, 23, 42, 56, 60, 143, 146], type: 'hard', description: 'CROSS: morning chaos → 6am/meditate/gym 5:30/dog bark 6am/5K/train 7:15/Chemex' },
]

// ═══════════════════════════════════════════════════════════════
// BENCHMARK
// ═══════════════════════════════════════════════════════════════

function checkHit(results: Memory[], expectedIndex: number | number[]): { hit: boolean; isTop1: boolean } {
  const resultContents = results.map(r => r.content)
  if (Array.isArray(expectedIndex)) {
    // Multi-match: pass if ANY expected memory appears in top-3
    const anyHit = expectedIndex.some(i => resultContents.includes(TEST_MEMORIES[i].content))
    const anyTop1 = expectedIndex.some(i => resultContents[0] === TEST_MEMORIES[i].content)
    return { hit: anyHit, isTop1: anyTop1 }
  }
  const expectedContent = TEST_MEMORIES[expectedIndex].content
  return {
    hit: resultContents.includes(expectedContent),
    isTop1: resultContents[0] === expectedContent,
  }
}

function runBenchmark() {
  console.log('═══════════════════════════════════════════════════════════')
  console.log('  cc-soul Vector-Free Recall Benchmark (English)')
  console.log(`  200 memories × 500 queries (200 direct + 200 semantic + 100 hard)`)
  console.log('═══════════════════════════════════════════════════════════')
  console.log()

  // Let AAM learn all test memories (simulating real usage)
  for (const mem of TEST_MEMORIES) {
    learnAssociation(mem.content, 0.3)
  }

  // Populate fact-store from test memories
  try {
    const factStore = require('./fact-store.ts')
    for (const mem of TEST_MEMORIES) {
      factStore.extractAndStoreFacts?.(mem.content, 'user')
    }
  } catch {}

  let directHits = 0, directTotal = 0
  let semanticHits = 0, semanticTotal = 0
  let hardHits = 0, hardTotal = 0
  let top1Hits = 0
  const failures: { query: string; type: string; desc: string; got: string[] }[] = []

  for (const tc of TEST_CASES) {
    const results = activationRecall(TEST_MEMORIES, tc.query, 3, 0, 0.5) as Memory[]
    const { hit, isTop1 } = checkHit(results, tc.expectedIndex)

    if (tc.type === 'direct') {
      directTotal++
      if (hit) directHits++
    } else if (tc.type === 'semantic') {
      semanticTotal++
      if (hit) semanticHits++
    } else {
      hardTotal++
      if (hit) hardHits++
    }
    if (isTop1) top1Hits++

    if (!hit) {
      failures.push({
        query: tc.query,
        type: tc.type,
        desc: tc.description,
        got: results.map(r => r.content.slice(0, 40)),
      })
    }

    const mark = hit ? (isTop1 ? '✅' : '🟡') : '❌'
    console.log(`${mark} [${tc.type.padEnd(8)}] ${tc.description.padEnd(40)} | ${tc.query}`)
  }

  console.log()
  console.log('═══════════════════════════════════════════════════════════')
  console.log('  Results')
  console.log('═══════════════════════════════════════════════════════════')
  console.log()
  const directRate = (directHits / directTotal * 100).toFixed(0)
  const semanticRate = (semanticHits / semanticTotal * 100).toFixed(0)
  const hardRate = (hardHits / hardTotal * 100).toFixed(0)
  const totalAll = directTotal + semanticTotal + hardTotal
  const hitsAll = directHits + semanticHits + hardHits
  const totalRate = (hitsAll / totalAll * 100).toFixed(0)
  const top1Rate = (top1Hits / totalAll * 100).toFixed(0)

  console.log(`  Direct recall (top-3):   ${directHits}/${directTotal} = ${directRate}%`)
  console.log(`  Semantic recall (top-3): ${semanticHits}/${semanticTotal} = ${semanticRate}%`)
  console.log(`  Hard recall (top-3):     ${hardHits}/${hardTotal} = ${hardRate}%`)
  console.log(`  Overall (top-3):         ${hitsAll}/${totalAll} = ${totalRate}%`)
  console.log(`  Top-1 accuracy:          ${top1Hits}/${totalAll} = ${top1Rate}%`)
  console.log()

  if (failures.length > 0) {
    console.log(`  ── Failed cases (${failures.length}) ──`)
    for (const f of failures) {
      console.log(`  ❌ [${f.type}] ${f.desc}: "${f.query}"`)
      console.log(`     Got: ${f.got.join(' | ')}`)
    }
  }
}

runBenchmark()
