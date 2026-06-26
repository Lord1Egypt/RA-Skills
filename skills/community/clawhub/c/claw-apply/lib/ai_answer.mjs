/**
 * ai_answer.mjs — AI-powered answer generation for unknown job application questions
 * Called when form_filler hits a question it can't answer from profile/answers.json
 */
import { readFileSync, existsSync } from 'fs';
import { ANTHROPIC_API_URL } from './constants.mjs';

/**
 * Generate an answer to an unknown application question using Claude.
 * @param {string} question - The question label/text from the form
 * @param {object} profile - Candidate profile (profile.json)
 * @param {string} apiKey - Anthropic API key
 * @param {object} job - Job context (title, company)
 * @returns {Promise<string|null>} - Suggested answer, or null on failure
 */
export async function generateAnswer(question, profile, apiKey, job = {}) {
  if (!apiKey) return null;

  // Read resume text if available — try pdftotext for PDFs, fall back to raw read
  let resumeText = '';
  if (profile.resume_path && existsSync(profile.resume_path)) {
    // Only attempt pdftotext for .pdf files
    if (profile.resume_path.toLowerCase().endsWith('.pdf')) {
      try {
        const { execFileSync } = await import('child_process');
        // execFileSync avoids shell injection — args passed as array, not interpolated
        resumeText = execFileSync('pdftotext', [profile.resume_path, '-'], { timeout: 3000 }).toString().slice(0, 4000);
      } catch {
        // pdftotext not available or failed — skip
      }
    } else {
      // Plain text resume
      try {
        resumeText = readFileSync(profile.resume_path, 'utf8').slice(0, 4000);
      } catch {
        // ignore
      }
    }
  }

  const candidateSummary = buildCandidateSummary(profile, resumeText);

  const systemPrompt = `You are helping a job candidate fill out application forms. Your job is to write answers that sound like a real person wrote them -- natural, direct, and specific to their background.

Rules:
- Use first person
- Be specific -- pull real details from the candidate's experience when relevant
- Keep answers concise but complete. For yes/no or short-answer fields, be brief. For behavioral questions, aim for 3-5 sentences.
- Do not use em dashes, the word "leverage", "delve", "utilize", "streamline", or phrases that sound like AI output
- Never make up facts. If you don't know something specific, answer honestly and generally
- Write like someone who is confident but not arrogant`;

  const userPrompt = `Candidate applying for: ${job.title || 'a sales role'} at ${job.company || 'a tech company'}

Candidate background:
${candidateSummary}

Application question:
"${question}"

Write the best answer for this question. Just the answer text -- no preamble, no explanation.`;

  try {
    const res = await fetch(ANTHROPIC_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 512,
        system: systemPrompt,
        messages: [{ role: 'user', content: userPrompt }],
      }),
    });

    if (!res.ok) return null;
    const data = await res.json();
    return data.content?.[0]?.text?.trim() || null;
  } catch {
    return null;
  }
}

function buildCandidateSummary(profile, resumeText) {
  const lines = [];

  const name = [profile.name?.first, profile.name?.last].filter(Boolean).join(' ');
  if (name) lines.push(`Name: ${name}`);
  if (profile.location?.city) lines.push(`Location: ${profile.location.city}, ${profile.location.state}`);
  if (profile.years_experience) lines.push(`Years of experience: ${profile.years_experience}`);
  if (profile.desired_salary) lines.push(`Target salary: $${profile.desired_salary.toLocaleString()}`);
  if (profile.work_authorization?.authorized) lines.push(`Work authorization: US authorized, no sponsorship required`);
  if (profile.willing_to_relocate === false) lines.push(`Relocation: not willing to relocate, remote only`);
  if (profile.linkedin_url) lines.push(`LinkedIn: ${profile.linkedin_url}`);

  if (profile.cover_letter) {
    lines.push(`\nBackground summary:\n${profile.cover_letter}`);
  }

  if (resumeText) {
    lines.push(`\nResume:\n${resumeText}`);
  }

  return lines.join('\n');
}
