const fs = require('fs');
const path = require('path');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function tokenize(text) {
  const stop = new Set(['the','and','for','with','from','you','your','job','jobs','engineering','engineer','executive','assistant','sr','sr.','jr','junior','officer','technician','maintenance','electrical','electronics','power','systems','bsc','bachelor']);
  return [...new Set(String(text).toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter(w => w.length > 3 && !stop.has(w)))];
}

function scoreJob(job, resumeTokens, prefs) {
  const text = JSON.stringify(job).toLowerCase();
  if (prefs.excludeSalesJobs && /sales|marketing/.test(text)) return -1;
  if (prefs.excludeTechnicianJobs && /technician/.test(text)) return -1;
  if (prefs.excludeDiplomaOnlyJobs && /diploma/.test(text) && !/bsc|bachelor/.test(text)) return -1;
  let s = 0;
  for (const t of resumeTokens) if (text.includes(t)) s += 1;
  const title = String(job.jobTitle || '').toLowerCase();
  if (/electrical|eee|instrument|automation|substation|power|maintenance|hvac|network & system|qualification & validation|network/.test(title)) s += 5;
  if (/bsc|bachelor|engineering/.test(text)) s += 2;
  return s;
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  const jobs = JSON.parse(fs.readFileSync(0, 'utf8'));
  const resume = fs.readFileSync(path.join(dataDir, 'resume.md'), 'utf8');
  const prefs = readJson(path.join(dataDir, 'preferences.json'));
  const applied = new Set(readJson(path.join(dataDir, 'appliedJobIds.json')).map(String));
  const tokens = tokenize(resume);
  const ranked = jobs.map(j => {
    const score = scoreJob(j, tokens, prefs);
    return { ...j, score };
  }).filter(j => j.score > 0 && !applied.has(String(j.jobId)))
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map(j => ({
      jobId: j.jobId,
      jobTitle: j.jobTitle,
      companyName: j.companyName,
      matchPercent: Math.min(100, j.score * 4),
      link: j.link,
      location: j.location,
      deadline: j.deadline
    }));

  fs.writeFileSync(path.join(dataDir, 'suggestedJobs.json'), JSON.stringify(ranked, null, 2) + '\n');
  console.log(JSON.stringify(ranked, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
