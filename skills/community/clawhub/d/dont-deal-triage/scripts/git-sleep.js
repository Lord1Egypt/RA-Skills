import path from "node:path";
import {
  SHORT_SLEEP_HOURS,
  HIGH_RISK_SLEEP_HOURS,
  addDays,
  average,
  diffHours,
  formatLocalIso,
  getLocalDateKey,
  longestConsecutive,
  pathExists,
  runCommand,
  startOfLocalDay
} from "./utils.js";

async function findNearestGitRepo(startDir) {
  let currentDir = path.resolve(startDir);

  while (true) {
    const gitPath = path.join(currentDir, ".git");
    if (await pathExists(gitPath)) {
      return currentDir;
    }

    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      return null;
    }

    currentDir = parentDir;
  }
}

async function readRecentCommits(repoPath, limit) {
  const { stdout } = await runCommand("git", ["-C", repoPath, "log", `--format=%aI`, "-n", String(limit)]);

  if (!stdout) {
    return [];
  }

  return stdout
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => new Date(line))
    .filter((date) => !Number.isNaN(date.getTime()))
    .sort((left, right) => left.getTime() - right.getTime());
}

async function repoHasCommits(repoPath) {
  try {
    await runCommand("git", ["-C", repoPath, "rev-parse", "--verify", "HEAD"]);
    return true;
  } catch {
    return false;
  }
}

function buildDayBuckets(commits, now, analyzedDays) {
  const windowEnd = startOfLocalDay(addDays(now, 1));
  const windowStart = startOfLocalDay(addDays(now, -(analyzedDays - 1)));

  const buckets = [];
  const bucketMap = new Map();

  for (let index = 0; index < analyzedDays; index += 1) {
    const day = addDays(windowStart, index);
    const key = getLocalDateKey(day);
    const bucket = {
      day: key,
      commits: [],
      start: null,
      end: null
    };
    buckets.push(bucket);
    bucketMap.set(key, bucket);
  }

  for (const commit of commits) {
    if (commit < windowStart || commit >= windowEnd) {
      continue;
    }

    const key = getLocalDateKey(commit);
    const bucket = bucketMap.get(key);
    if (!bucket) {
      continue;
    }

    bucket.commits.push(commit);
  }

  for (const bucket of buckets) {
    if (bucket.commits.length === 0) {
      continue;
    }

    bucket.start = bucket.commits[0];
    bucket.end = bucket.commits[bucket.commits.length - 1];
  }

  return buckets;
}

function deriveSleepWindows(dayBuckets) {
  const windows = [];

  for (let index = 1; index < dayBuckets.length; index += 1) {
    const previous = dayBuckets[index - 1];
    const current = dayBuckets[index];

    if (!previous.end || !current.start) {
      continue;
    }

    const hours = diffHours(previous.end, current.start);
    if (hours < 0 || hours > 24) {
      continue;
    }

    windows.push({
      previous_day: previous.day,
      current_day: current.day,
      sleep_hours_est: hours,
      short_sleep: hours < SHORT_SLEEP_HOURS,
      from_last_commit: formatLocalIso(previous.end),
      to_first_commit: formatLocalIso(current.start)
    });
  }

  return windows;
}

function deriveRisk(sleepWindows) {
  if (sleepWindows.length === 0) {
    return {
      shortSleepDays: 0,
      averageSleepHours: null,
      lastSleepHours: null,
      longestShortStreak: 0,
      riskFlag: "unknown",
      latestWindow: null
    };
  }

  const shortSleepDays = sleepWindows.filter((window) => window.short_sleep).length;
  const averageSleepHours = average(sleepWindows.map((window) => window.sleep_hours_est));
  const lastWindow = sleepWindows[sleepWindows.length - 1];
  const lastSleepHours = lastWindow.sleep_hours_est;
  const longestShortStreak = longestConsecutive(sleepWindows, (window) => window.short_sleep);

  let riskFlag = "low";
  if (
    shortSleepDays >= 3 ||
    lastSleepHours < HIGH_RISK_SLEEP_HOURS ||
    longestShortStreak >= 2
  ) {
    riskFlag = "high";
  } else if (shortSleepDays >= 1 || lastSleepHours < SHORT_SLEEP_HOURS) {
    riskFlag = "moderate";
  }

  return {
    shortSleepDays,
    averageSleepHours,
    lastSleepHours,
    longestShortStreak,
    riskFlag,
    latestWindow: lastWindow
  };
}

export async function inferSleepFromGit(options = {}) {
  const {
    cwd = process.cwd(),
    analyzedDays = 7,
    commitLimit = 120
  } = options;

  const repoPath = await findNearestGitRepo(cwd);

  if (!repoPath) {
    return {
      repository_path: null,
      analyzed_days: analyzedDays,
      commits_seen: 0,
      short_sleep_days: 0,
      average_sleep_hours_est: null,
      last_sleep_hours_est: null,
      longest_short_sleep_streak: 0,
      last_sleep_window: null,
      recent_nights: [],
      risk_flag: "unknown",
      note: "No git repository found from the current working directory upward."
    };
  }

  try {
    const hasCommits = await repoHasCommits(repoPath);
    if (!hasCommits) {
      return {
        repository_path: repoPath,
        analyzed_days: analyzedDays,
        commits_seen: 0,
        short_sleep_days: 0,
        average_sleep_hours_est: null,
        last_sleep_hours_est: null,
        longest_short_sleep_streak: 0,
        last_sleep_window: null,
        recent_nights: [],
        risk_flag: "unknown",
        note: "Git repository found, but there are no commits yet."
      };
    }

    const commits = await readRecentCommits(repoPath, commitLimit);
    const dayBuckets = buildDayBuckets(commits, new Date(), analyzedDays);
    const sleepWindows = deriveSleepWindows(dayBuckets);
    const risk = deriveRisk(sleepWindows);

    return {
      repository_path: repoPath,
      analyzed_days: analyzedDays,
      commits_seen: commits.length,
      short_sleep_days: risk.shortSleepDays,
      average_sleep_hours_est: risk.averageSleepHours,
      last_sleep_hours_est: risk.lastSleepHours,
      longest_short_sleep_streak: risk.longestShortStreak,
      last_sleep_window: risk.latestWindow,
      recent_nights: sleepWindows,
      risk_flag: risk.riskFlag
    };
  } catch (error) {
    return {
      repository_path: repoPath,
      analyzed_days: analyzedDays,
      commits_seen: 0,
      short_sleep_days: 0,
      average_sleep_hours_est: null,
      last_sleep_hours_est: null,
      longest_short_sleep_streak: 0,
      last_sleep_window: null,
      recent_nights: [],
      risk_flag: "unknown",
      note: `Failed to read git history: ${error.message}`
    };
  }
}
