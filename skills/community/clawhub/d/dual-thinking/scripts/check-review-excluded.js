const { listTextFiles } = require('/home/irtual/.npm-global/lib/node_modules/clawhub/dist/skills.js');
(async () => {
  const files = await listTextFiles('/home/irtual/.openclaw/workspace/skills/dual-thinking');
  const hasReview = files.some(f => f.relPath.startsWith('review/'));
  console.log(hasReview ? 'REVIEW_INCLUDED' : 'REVIEW_EXCLUDED');
  process.exit(hasReview ? 1 : 0);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
