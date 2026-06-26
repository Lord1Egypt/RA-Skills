#!/usr/bin/env node
import { ensureStateDir, getQueuedFeeds } from "./common.mjs";

await ensureStateDir();
const feeds = await getQueuedFeeds();

if (feeds.length === 0) {
  console.log("NO_NEW_FEEDS");
  process.exit(0);
}

console.log(`NEW_FEEDS: ${feeds.length}`);
console.log("");
console.log(JSON.stringify({ feeds }));
