const https = require('https');
const { URL } = require('url');

function requestJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, { method: 'GET', headers: { 'User-Agent': 'OpenClaw/BDJobsSkill' } }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve({ statusCode: res.statusCode, body: JSON.parse(body) }); }
        catch { resolve({ statusCode: res.statusCode, body }); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

function buildSearchUrl({ keyword, isFresher, pg, jobLocation, postedWithin }) {
  const u = new URL('https://api.bdjobs.com/Jobs/api/JobSearch/GetJobSearch');
  const params = {
    Icat: '', industry: '', category: '', org: '', jobNature: '', Fcat: '', location: jobLocation || '',
    Qot: '', jobType: '', jobLevel: '', postedWithin: String(postedWithin || ''), deadline: '', keyword: keyword || '', pg: String(pg || 1),
    qAge: '', Salary: '', experience: '', gender: '', MExp: '', genderB: '', MPostings: '', MCat: '', version: '',
    rpp: '50', Newspaper: '', armyp: '', QDisablePerson: '', pwd: '', workplace: '', facilitiesForPWD: '',
    SaveFilterList: '', UserFilterName: '', HUserFilterName: '', earlyJobAccess: '', isPro: '0', ToggleJobs: 'true',
    isFresher: isFresher ? 'true' : 'false'
  };
  Object.entries(params).forEach(([k, v]) => u.searchParams.set(k, v));
  return u.toString();
}

(async () => {
  const keyword = process.argv.find(v => v.startsWith('--keyword='))?.split('=')[1] || '';
  const isFresher = (process.argv.find(v => v.startsWith('--isFresher='))?.split('=')[1] || 'true') === 'true';
  const pages = Number(process.argv.find(v => v.startsWith('--pages='))?.split('=')[1] || '1') || 1;
  const jobLocation = process.argv.find(v => v.startsWith('--jobLocation='))?.split('=')[1] || '';
  const postedWithin = Number(process.argv.find(v => v.startsWith('--postedWithin='))?.split('=')[1] || '') || '';

  const out = [];
  for (let pg = 1; pg <= pages; pg++) {
    const url = buildSearchUrl({ keyword, isFresher, pg, jobLocation, postedWithin });
    const res = await requestJson(url);
    const jobs = Array.isArray(res.body?.data) ? res.body.data : [];
    out.push(...jobs.map(job => ({
      jobId: job.Jobid,
      jobTitle: job.jobTitle,
      companyName: job.companyName,
      location: job.location,
      deadline: job.deadline,
      link: `https://bdjobs.com/h/details/${job.Jobid}`,
      pg
    })));
  }

  console.log(JSON.stringify(out, null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
