import { loadQueue } from "./lib/queue.mjs";
const q = loadQueue();

// Composite IDs
const composite = q.filter(j => j.id.includes("_gtm") || j.id.includes("_ae"));
console.log("Composite IDs:", composite.length);
if (composite.length > 0) {
  const scored = composite.filter(j => j.filter_score !== null && j.filter_score !== undefined);
  console.log("  Scored:", scored.length);
  console.log("  Sample:", composite[0].id, "status:", composite[0].status, "score:", composite[0].filter_score);
}

// Filter submit timestamps
const timestamps = [...new Set(q.map(j => j.filter_submitted_at).filter(Boolean))].sort();
console.log("\nFilter submit timestamps:", timestamps.length);
for (const t of timestamps) {
  const jobs = q.filter(j => j.filter_submitted_at === t);
  const noScore = jobs.filter(j => j.filter_score === null || j.filter_score === undefined);
  console.log(" ", t, ":", jobs.length, "jobs,", noScore.length, "unscored");
}

// The key question: after the last collect, were there jobs with status=new and no score?
// Simulate what submit() sees
const wouldSubmit = q.filter(j => j.status === "new" && (j.filter_score === null || j.filter_score === undefined) && !j.filter_batch_id && !j.filter_submitted_at);
console.log("\nWould submit now:", wouldSubmit.length);

// Check: are there jobs with filter_score explicitly set to null (error case)?
const explicitNull = q.filter(j => j.filter_score === null);
console.log("Explicit filter_score=null:", explicitNull.length);
if (explicitNull.length > 0) {
  console.log("  Statuses:", JSON.stringify([...new Set(explicitNull.map(j => j.status))]));
  console.log("  Sample:", explicitNull[0].id, "status:", explicitNull[0].status, "reason:", explicitNull[0].filter_reason, "batch:", explicitNull[0].filter_batch_id);
}

// What about undefined?
const noScoreAtAll = q.filter(j => j.filter_score === undefined);
console.log("filter_score=undefined:", noScoreAtAll.length);

process.exit(0);
