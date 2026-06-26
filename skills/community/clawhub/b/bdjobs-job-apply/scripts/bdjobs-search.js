const fs = require('fs');
const path = require('path');
const https = require('https');
const { URL } = require('url');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

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
    Qot: '', jobType: '', jobLevel: '', deadline: '', keyword: keyword || '', pg: String(pg || 1),
    qAge: '', Salary: '', experience: '', gender: '', MExp: '', genderB: '', MPostings: '', MCat: '', version: '',
    rpp: '50', Newspaper: '', armyp: '', QDisablePerson: '', pwd: '', workplace: '', facilitiesForPWD: '',
    SaveFilterList: '', UserFilterName: '', HUserFilterName: '', earlyJobAccess: '', isPro: '0', ToggleJobs: 'true',
    isFresher: isFresher ? 'true' : 'false'
  };
  if (postedWithin !== undefined && postedWithin !== null && postedWithin !== '') params.postedWithin = String(postedWithin);
  Object.entries(params).forEach(([k, v]) => u.searchParams.set(k, v));
  return u.toString();
}

function loadPreferences(root) {
  const prefPath = path.join(root, 'data', 'preferences.json');
  return fs.existsSync(prefPath) ? readJson(prefPath) : {};
}

function loadResume(root) {
  const resumePath = path.join(root, 'data', 'resume.md');
  return fs.existsSync(resumePath) ? fs.readFileSync(resumePath, 'utf8') : '';
}

function extractText(job) {
  return [
    job.JobTitle,
    job.CompanyName,
    job.JobDescription,
    job.EducationRequirements,
    job.experience,
    job.AdditionJobRequirements,
    job.JobLocation,
    job.SuggestedSkills,
    job.JobNature
  ].filter(Boolean).join('\n');
}

function heuristicsBlock(details, prefs) {
  const text = extractText(details).toLowerCase();
  if (prefs.excludeSalesJobs && /sales|marketing/i.test(text)) return true;
  if (prefs.excludeTechnicianJobs && /technician/i.test(text)) return true;
  if (prefs.excludeDiplomaOnlyJobs && /diploma/i.test(text) && !/bsc|bachelor/i.test(text)) return true;
  return false;
}

async function getJobDetails(jobId) {
  const url = new URL('https://gateway.bdjobs.com/jobapply/api/JobSubsystem/Job-Details');
  url.searchParams.set('jobId', String(jobId));
  const res = await requestJson(url.toString());
  return res.body?.data?.[0] || null;
}

async function refreshAppliedJobIds(root) {
  const dataDir = path.join(root, 'data');
  const logged = readJson(path.join(dataDir, 'loggedInData.json'));
  const user = readJson(path.join(dataDir, 'userDetails.json'));
  const guidId = logged.guidId || user.guidId;
  const collected = [];
  let page = 1;
  let totalPages = 1;
  while (page <= totalPages) {
    const url = new URL('https://useractivitysubsystem-odcx6humqq-as.a.run.app/api/AppliedJob/GetApplyPositionInfoV1');
    url.searchParams.set('UserGuid', guidId);
    url.searchParams.set('Version', 'EN');
    url.searchParams.set('PageNumber', String(page));
    url.searchParams.set('NoOfRecordPerPage', '20');
    const res = await requestJson(url.toString());
    const value = res.body?.event?.eventData?.[0]?.value;
    const data = Array.isArray(value?.data) ? value.data : [];
    totalPages = Number(value?.common?.totalNumberOfPage || totalPages);
    for (const item of data) collected.push(Number(item.jobId));
    page += 1;
  }
  writeJson(path.join(dataDir, 'appliedJobIds.json'), [...new Set(collected)]);
}

(async () => {
  const root = process.cwd();
  const dataDir = path.join(root, 'data');
  await refreshAppliedJobIds(root);
  const userDetails = readJson(path.join(dataDir, 'userDetails.json'));
  const prefs = loadPreferences(root);
  const resumeText = loadResume(root);
  const appliedIds = new Set((readJson(path.join(dataDir, 'appliedJobIds.json')) || []).map(String));
  const notLikedPath = path.join(dataDir, 'not-liked-job-list.json');
  const notLikedIds = new Set((fs.existsSync(notLikedPath) ? readJson(notLikedPath) : []).map(String));
  const rawKeywords = process.argv.find(v => v.startsWith('--keywords='))?.split('=')[1];
  const keywords = (rawKeywords ? rawKeywords.split(',') : (prefs.searchKeywords || [])).map(s => s.trim()).filter(Boolean);
  const pages = Number(process.argv.find(v => v.startsWith('--pages='))?.split('=')[1] || '4') || 4;
  const isFresher = (process.argv.find(v => v.startsWith('--isFresher='))?.split('=')[1] || String(userDetails.isFresher)) === 'true';
  const jobLocation = process.argv.find(v => v.startsWith('--jobLocation='))?.split('=')[1] || userDetails.jobLocation || '';
  const postedWithinArg = process.argv.find(v => v.startsWith('--postedWithin='))?.split('=')[1];
  const postedWithin = postedWithinArg !== undefined ? Number(postedWithinArg) : undefined;

  const outJobs = [];
  const seen = new Set();
  for (let pg = 1; pg <= pages; pg++) {
    for (const keyword of keywords) {
      const url = buildSearchUrl({ keyword, isFresher, pg, jobLocation, postedWithin });
      const res = await requestJson(url);
      const jobs = Array.isArray(res.body?.data) ? res.body.data : [];
      for (const job of jobs) {
        const id = String(job.Jobid);
        if (appliedIds.has(id) || notLikedIds.has(id) || seen.has(id)) continue;
        seen.add(id);
        const details = await getJobDetails(job.Jobid);
        if (!details) continue;
        if (heuristicsBlock(details, prefs)) continue;
        outJobs.push({
          jobId: job.Jobid,
          jobTitle: details.JobTitle || job.jobTitle,
          companyName: details.CompanyName || job.companyName,
          link: `https://bdjobs.com/h/details/${job.Jobid}`,
          location: details.JobLocation || job.location || '',
          deadline: details.Deadline || job.deadline || '',
          details,
          resumeText
        });
      }
    }
  }

  const unique = [...new Map(outJobs.map(j => [String(j.jobId), j])).values()];
  console.log(JSON.stringify(unique.slice(0, 50), null, 2));
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
