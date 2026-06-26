#!/usr/bin/env node
/**
 * AI Job Hunter - Scan remote job boards
 */

const https = require('https');

const JOB_SOURCES = [
  {
    name: 'RemoteOK',
    url: 'https://remoteok.com/api',
    parser: (data) => JSON.parse(data).slice(1).map(j => ({
      title: j.position,
      company: j.company,
      salary: j.salary_min ? `$${j.salary_min}-${j.salary_max}` : 'Not specified',
      url: j.url,
      tags: j.tags || [],
      date: j.date
    }))
  }
];

async function fetchJobs(source) {
  return new Promise((resolve, reject) => {
    https.get(source.url, { headers: { 'User-Agent': 'OpenClaw-JobHunter/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(source.parser(data));
        } catch (e) {
          resolve([]);
        }
      });
    }).on('error', () => resolve([]));
  });
}

function filterJobs(jobs, keywords) {
  const kw = keywords.toLowerCase().split(/\s+/);
  return jobs.filter(job => {
    const text = `${job.title} ${job.company} ${job.tags.join(' ')}`.toLowerCase();
    return kw.some(k => text.includes(k));
  });
}

function formatOutput(jobs) {
  if (jobs.length === 0) return 'No matching jobs found.';
  
  return jobs.slice(0, 10).map((job, i) => 
    `${i+1}. **${job.title}** @ ${job.company}\n   💰 ${job.salary}\n   🔗 ${job.url}`
  ).join('\n\n');
}

async function main() {
  const keywords = process.argv.slice(2).join(' ') || 'developer engineer';
  console.log(`🔍 Searching for: ${keywords}\n`);
  
  let allJobs = [];
  for (const source of JOB_SOURCES) {
    const jobs = await fetchJobs(source);
    allJobs = allJobs.concat(jobs);
  }
  
  const filtered = filterJobs(allJobs, keywords);
  console.log(formatOutput(filtered));
  console.log(`\n📊 Found ${filtered.length} matching jobs from ${allJobs.length} total`);
}

main().catch(console.error);
