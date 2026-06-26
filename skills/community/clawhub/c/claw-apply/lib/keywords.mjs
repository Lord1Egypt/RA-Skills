/**
 * keywords.mjs — AI-generated search keywords
 * One Claude call per search track using full profile + search config context
 */

import { ANTHROPIC_API_URL } from './constants.mjs';

export async function generateKeywords(search, profile, apiKey) {
  if (!apiKey) throw new Error('ANTHROPIC_API_KEY not set');

  const prompt = `You are an expert job search strategist helping a candidate find the right roles on LinkedIn and Wellfound.

## Candidate Profile
- Name: ${profile.name.first} ${profile.name.last}
- Location: ${profile.location.city}, ${profile.location.state} (remote only)
- Years experience: ${profile.years_experience}
- Desired salary: $${profile.desired_salary.toLocaleString()}
- Work authorization: Authorized to work in US + UK, no sponsorship needed
- Willing to relocate: ${profile.willing_to_relocate ? 'Yes' : 'No'}
- Background summary: ${profile.cover_letter?.substring(0, 400)}

## Job Search Track: "${search.name}"
- Salary minimum: $${(search.salary_min || 0).toLocaleString()}
- Platforms: ${(search.platforms || []).join(', ')}
- Remote only: ${search.filters?.remote ? 'Yes' : 'No'}
- Exclude these keywords: ${(search.exclude_keywords || []).join(', ')}
- Current keywords already in use: ${(search.keywords || []).join(', ')}

## Task
Generate 15 additional LinkedIn/Wellfound job search query strings to find "${search.name}" roles for this candidate.

Think about:
- How do startups and hiring managers actually title these roles at seed/Series A/B companies?
- What variations exist across industries (fintech, devtools, data infra, security, AI/ML)?
- What seniority + function combinations surface the best matches?
- What terms does this specific candidate's background match well?
- Do NOT repeat keywords already listed above
- Do NOT use excluded keywords

Return ONLY a JSON array of strings, no explanation, no markdown.
Example format: ["query one", "query two", "query three"]`;

  const res = await fetch(ANTHROPIC_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 1024,
      messages: [{ role: 'user', content: prompt }]
    })
  });

  if (!res.ok) throw new Error(`Anthropic API error: ${res.status} ${res.statusText}`);

  const data = await res.json();
  if (data.error) throw new Error(data.error.message);
  if (!data.content?.[0]?.text) throw new Error('Unexpected API response: missing content');

  const text = data.content[0].text.trim();
  const clean = text.replace(/```json\n?|\n?```/g, '').trim();
  return JSON.parse(clean);
}
