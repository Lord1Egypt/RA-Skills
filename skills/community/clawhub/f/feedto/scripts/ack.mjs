#!/usr/bin/env node
import { removeQueuedFeedIds } from "./common.mjs";

const ids = process.argv.slice(2);
await removeQueuedFeedIds(ids);
