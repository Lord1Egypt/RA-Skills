#!/usr/bin/env node

const fs = require("node:fs");
const { spawnSync } = require("node:child_process");

const DEFAULT_SAMPLE_RATE = 22050;
const DEFAULT_MIN_TEMPO = 70;
const DEFAULT_MAX_TEMPO = 180;
const TARGET_FRAME_RATE = 200;
const LONG_TRACK_THRESHOLD_SECONDS = 15;
const PRIMARY_WINDOW_SECONDS = 10;
const SUPPLEMENTAL_WINDOW_SECONDS = 6;

function parseArgs(argv) {
  const args = {};

  for (let index = 2; index < argv.length; index += 1) {
    const part = argv[index];

    if (!part.startsWith("--")) {
      continue;
    }

    const key = part.slice(2);
    const next = argv[index + 1];

    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }

    args[key] = next;
    index += 1;
  }

  return args;
}

function parseNumberList(input, label) {
  if (typeof input !== "string" || input.trim() === "") {
    throw new Error(`${label} input is required.`);
  }

  const values = input
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => Number(item));

  if (values.length === 0) {
    throw new Error(`${label} input is required.`);
  }

  if (values.some((value) => !Number.isFinite(value))) {
    throw new Error(`${label} must contain only numeric values.`);
  }

  return values;
}

function parsePositiveNumber(input, fallback, label) {
  if (input === undefined) {
    return fallback;
  }

  const value = Number(input);
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error(`${label} must be a positive number.`);
  }

  return value;
}

function parseOptionalNumber(input, label) {
  if (input === undefined) {
    return undefined;
  }

  const value = Number(input);
  if (!Number.isFinite(value)) {
    throw new Error(`${label} must be a numeric value.`);
  }

  return value;
}

function median(values) {
  const sorted = [...values].sort((left, right) => left - right);
  const middle = Math.floor(sorted.length / 2);

  if (sorted.length % 2 === 0) {
    return (sorted[middle - 1] + sorted[middle]) / 2;
  }

  return sorted[middle];
}

function round(value, precision = 2) {
  return Number(value.toFixed(precision));
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function analyzeIntervals(intervals) {
  if (intervals.length < 1) {
    throw new Error("At least one interval is required.");
  }

  if (intervals.some((value) => value <= 0)) {
    throw new Error("Intervals must be greater than 0.");
  }

  const averageIntervalMs =
    intervals.reduce((sum, value) => sum + value, 0) / intervals.length;
  const medianIntervalMs = median(intervals);

  return {
    source: "intervals",
    bpm: round(60000 / averageIntervalMs),
    averageIntervalMs: round(averageIntervalMs),
    medianIntervalMs: round(medianIntervalMs),
    tapCount: intervals.length + 1,
  };
}

function analyzeTimestamps(timestamps) {
  if (timestamps.length < 2) {
    throw new Error("At least two timestamps are required.");
  }

  if (timestamps.some((value) => value < 0)) {
    throw new Error("Timestamps must be greater than or equal to 0.");
  }

  const intervals = [];
  for (let index = 1; index < timestamps.length; index += 1) {
    const interval = timestamps[index] - timestamps[index - 1];

    if (interval <= 0) {
      throw new Error("Timestamps must be strictly increasing.");
    }

    intervals.push(interval);
  }

  const analysis = analyzeIntervals(intervals);

  return {
    ...analysis,
    source: "timestamps",
    tapCount: timestamps.length,
  };
}

function buildMonoAudioProfile(audioData, sampleRate) {
  return {
    samples: audioData,
    sampleRate,
    duration: audioData.length / sampleRate,
  };
}

function buildOnsetEnvelope(monoProfile, window) {
  const startSample = Math.floor(window.offset * monoProfile.sampleRate);
  const endSample = Math.min(
    monoProfile.samples.length,
    Math.floor((window.offset + window.duration) * monoProfile.sampleRate)
  );
  const mono = monoProfile.samples.subarray(startSample, endSample);

  if (mono.length < 512) {
    return null;
  }

  let mean = 0;
  for (let index = 0; index < mono.length; index += 1) {
    mean += mono[index];
  }
  mean /= mono.length;

  const hopSize = Math.max(1, Math.floor(monoProfile.sampleRate / TARGET_FRAME_RATE));
  const frameSize = Math.max(hopSize * 4, 256);
  const frameCount = Math.floor((mono.length - frameSize) / hopSize) + 1;

  if (frameCount < 32) {
    return null;
  }

  const energies = new Float32Array(frameCount);
  for (let frame = 0; frame < frameCount; frame += 1) {
    const start = frame * hopSize;
    let sum = 0;
    for (let index = 0; index < frameSize; index += 1) {
      sum += Math.abs(mono[start + index] - mean);
    }
    energies[frame] = sum / frameSize;
  }

  const envelope = new Float32Array(frameCount - 1);
  let adaptiveMean = energies[0];
  let maxValue = 0;

  for (let index = 1; index < frameCount; index += 1) {
    const flux = Math.max(0, energies[index] - energies[index - 1]);
    adaptiveMean = adaptiveMean * 0.98 + flux * 0.02;
    const value = Math.max(0, flux - adaptiveMean * 0.9);
    envelope[index - 1] = value;
    if (value > maxValue) {
      maxValue = value;
    }
  }

  if (maxValue <= 1e-8) {
    return null;
  }

  const invMax = 1 / maxValue;
  for (let index = 0; index < envelope.length; index += 1) {
    envelope[index] = clamp(envelope[index] * invMax, 0, 1);
  }

  return {
    envelope,
    frameRate: monoProfile.sampleRate / hopSize,
  };
}

function computeAutocorrelation(envelope, minLag, maxLag) {
  const autocorrelation = new Float32Array(maxLag + 1);

  for (let lag = minLag; lag <= maxLag; lag += 1) {
    let dot = 0;
    let leftPower = 0;
    let rightPower = 0;

    for (let index = lag; index < envelope.length; index += 1) {
      const left = envelope[index];
      const right = envelope[index - lag];
      dot += left * right;
      leftPower += left * left;
      rightPower += right * right;
    }

    if (leftPower > 0 && rightPower > 0) {
      autocorrelation[lag] = dot / Math.sqrt(leftPower * rightPower);
    }
  }

  return autocorrelation;
}

function harmonicEnhancement(autocorrelation, lag, subharmonicWeight = 0) {
  let score = autocorrelation[lag] || 0;

  if (subharmonicWeight > 0) {
    const halfLag = Math.round(lag / 2);
    if (halfLag >= 2 && halfLag < autocorrelation.length) {
      score += subharmonicWeight * autocorrelation[halfLag];
    }
  }

  if (lag * 2 < autocorrelation.length) {
    score += 0.35 * autocorrelation[lag * 2];
  }

  if (lag * 4 < autocorrelation.length) {
    score += 0.15 * autocorrelation[lag * 4];
  }

  return score;
}

function computePulseTrainScore(envelope, period) {
  if (period < 2) {
    return { score: 0, phase: 0 };
  }

  const maxPhase = Math.max(1, Math.round(period));
  const phaseStep = Math.max(1, Math.floor(maxPhase / 8));
  let bestScore = 0;
  let bestPhase = 0;

  for (let phase = 0; phase < maxPhase; phase += phaseStep) {
    let sum = 0;
    let count = 0;

    for (let cursor = phase; cursor < envelope.length; cursor += period) {
      const index = Math.round(cursor);
      if (index < envelope.length) {
        sum += envelope[index];
        count += 1;
      }
    }

    if (count >= 3) {
      const score = sum / count;
      if (score > bestScore) {
        bestScore = score;
        bestPhase = phase;
      }
    }
  }

  return { score: clamp(bestScore, 0, 1), phase: bestPhase };
}

function scoreTempoCandidate(envelope, frameRate, tempo, autocorrelation) {
  if (!Number.isFinite(tempo) || tempo <= 0) {
    return null;
  }

  const lag = Math.round((60 * frameRate) / tempo);
  if (lag < 2 || lag >= envelope.length - 1) {
    return null;
  }

  const periodicityScore = clamp(autocorrelation[lag] ?? 0, 0, 1);
  const subharmonicWeight = tempo >= 130 ? 0.35 : 0;
  const harmonicScore = clamp(
    harmonicEnhancement(autocorrelation, lag, subharmonicWeight),
    0,
    1.75
  );
  const pulse = computePulseTrainScore(envelope, (60 * frameRate) / tempo);
  const score = clamp(
    harmonicScore * 0.3 + pulse.score * 0.45 + periodicityScore * 0.25,
    0,
    2.2
  );

  return {
    tempo,
    lag,
    phase: pulse.phase,
    periodicityScore,
    harmonicScore,
    pulseScore: pulse.score,
    score,
    support: 0,
  };
}

function dedupeCandidates(candidates) {
  const sorted = [...candidates].sort((left, right) => right.score - left.score);
  const deduped = [];

  for (const candidate of sorted) {
    const exists = deduped.some(
      (current) => Math.abs(current.tempo - candidate.tempo) <= 0.8
    );
    if (!exists) {
      deduped.push(candidate);
    }
  }

  return deduped;
}

function collectTempoCandidates(envelope, frameRate, minTempo, maxTempo, limit = 8) {
  const minLag = clamp(
    Math.round((60 * frameRate) / maxTempo),
    2,
    envelope.length - 2
  );
  const maxLag = clamp(
    Math.round((60 * frameRate) / minTempo),
    minLag + 1,
    envelope.length - 2
  );
  const autocorrelation = computeAutocorrelation(envelope, minLag, maxLag);
  const lagPeaks = [];

  for (let lag = minLag + 1; lag < maxLag; lag += 1) {
    const current = harmonicEnhancement(autocorrelation, lag);
    const left = harmonicEnhancement(autocorrelation, lag - 1);
    const right = harmonicEnhancement(autocorrelation, lag + 1);

    if (current >= left && current >= right) {
      lagPeaks.push(lag);
    }
  }

  lagPeaks.sort(
    (left, right) =>
      harmonicEnhancement(autocorrelation, right) -
      harmonicEnhancement(autocorrelation, left)
  );

  const rawCandidates = [];
  for (const lag of lagPeaks.slice(0, Math.max(limit * 3, 18))) {
    const tempo = (60 * frameRate) / lag;
    const candidate = scoreTempoCandidate(envelope, frameRate, tempo, autocorrelation);
    if (candidate) {
      rawCandidates.push(candidate);
    }
  }

  return {
    candidates: dedupeCandidates(rawCandidates).slice(0, limit),
    autocorrelation,
  };
}

function logTempoPrior(tempo, center = 120, widthOctaves = 1.2) {
  const distance = Math.log2(Math.max(1e-6, tempo / center));
  return Math.exp(-(distance * distance) / (2 * widthOctaves * widthOctaves));
}

function resolveOctaveAmbiguity(candidates, envelope, frameRate, autocorrelation, minTempo, maxTempo) {
  if (candidates.length === 0) {
    return [];
  }

  const tempoFamily = [];
  for (const candidate of candidates.slice(0, 3)) {
    for (const factor of [1, 2, 0.5, 4 / 3]) {
      const tempo = candidate.tempo * factor;
      if (tempo >= minTempo && tempo <= maxTempo) {
        tempoFamily.push(tempo);
      }
    }
  }

  const uniqueTempos = [...tempoFamily]
    .sort((left, right) => left - right)
    .filter(
      (tempo, index, list) =>
        index === 0 || Math.abs(list[index - 1] - tempo) > 0.8
    );

  const rescored = [];
  for (const tempo of uniqueTempos) {
    const candidate = scoreTempoCandidate(envelope, frameRate, tempo, autocorrelation);
    if (!candidate) {
      continue;
    }

    candidate.score *= 0.85 + 0.15 * logTempoPrior(candidate.tempo);
    rescored.push(candidate);
  }

  for (const candidate of rescored) {
    if (candidate.tempo >= 150) {
      const half = rescored.find((item) => Math.abs(item.tempo - candidate.tempo / 2) <= 1.2);
      if (half && half.score >= candidate.score * 0.82) {
        candidate.score *= 0.68;
      }
    }

    if (candidate.tempo >= 132 && candidate.tempo <= 148) {
      const threeQuarter = rescored.find(
        (item) => Math.abs(item.tempo - candidate.tempo * 0.75) <= 1.2
      );
      if (threeQuarter && threeQuarter.score >= candidate.score * 0.88) {
        candidate.score *= 0.9;
      }
    }
  }

  return rescored.sort((left, right) => right.score - left.score);
}

function shouldRunSupplemental(best, second) {
  if (!best || !second) {
    return false;
  }

  return best.score < 0.38 || best.score - second.score < 0.06;
}

function resolvePrimaryWindow(durationSeconds, offset, duration) {
  if (offset !== undefined || duration !== undefined) {
    const start = clamp(offset ?? 0, 0, Math.max(0, durationSeconds - 0.25));
    const maxDuration = Math.max(0.25, durationSeconds - start);
    const selectedDuration = clamp(duration ?? maxDuration, 0.25, maxDuration);
    return { offset: start, duration: selectedDuration };
  }

  if (durationSeconds <= LONG_TRACK_THRESHOLD_SECONDS) {
    return { offset: 0, duration: durationSeconds };
  }

  const windowDuration = Math.min(PRIMARY_WINDOW_SECONDS, durationSeconds);
  return {
    offset: Math.max(0, (durationSeconds - windowDuration) / 2),
    duration: windowDuration,
  };
}

function buildSupplementalWindows(durationSeconds, primaryWindow) {
  if (durationSeconds <= LONG_TRACK_THRESHOLD_SECONDS) {
    return [];
  }

  const duration = Math.min(SUPPLEMENTAL_WINDOW_SECONDS, durationSeconds);
  const maxOffset = Math.max(0, durationSeconds - duration);

  return [0.2, 0.7]
    .map((anchor) => {
      const center = durationSeconds * anchor;
      const offset = clamp(center - duration / 2, 0, maxOffset);
      return { offset, duration };
    })
    .filter((window) => Math.abs(window.offset - primaryWindow.offset) > 1);
}

function calculateConfidence(best, second, consistency) {
  const normalizedScore = clamp((best.score - 0.1) / 0.55, 0, 1);
  const margin = second
    ? clamp((best.score - second.score) / Math.max(0.015, best.score * 0.65), 0, 1)
    : 1;
  const pulseStrength = clamp(best.pulseScore, 0, 1);
  const periodicity = clamp(best.periodicityScore, 0, 1);

  const blended =
    normalizedScore * 0.34 +
    margin * 0.16 +
    consistency * 0.18 +
    pulseStrength * 0.18 +
    periodicity * 0.14;

  let calibrated = 58 + Math.pow(clamp(blended, 0, 1), 0.78) * 36;

  if (consistency >= 0.95) {
    calibrated += 3;
  }

  if (pulseStrength >= 0.55 && periodicity >= 0.4) {
    calibrated += 2;
  }

  return Math.round(clamp(calibrated, 58, 96));
}

function readF32LEBuffer(buffer) {
  if (buffer.length % 4 !== 0) {
    throw new Error("Decoded audio buffer is not aligned to 32-bit float frames.");
  }

  const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);
  const samples = new Float32Array(buffer.length / 4);

  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = view.getFloat32(index * 4, true);
  }

  return samples;
}

let resolvedFfmpegBinary = null;

function resolveFfmpegBinary() {
  if (resolvedFfmpegBinary) {
    return resolvedFfmpegBinary;
  }

  const candidates = [];
  const seen = new Set();
  const pushCandidate = (candidate) => {
    if (!candidate || seen.has(candidate)) {
      return;
    }
    seen.add(candidate);
    candidates.push(candidate);
  };

  if (process.env.FFMPEG_PATH) {
    pushCandidate(process.env.FFMPEG_PATH);
  }

  pushCandidate("/opt/homebrew/bin/ffmpeg");
  pushCandidate("/usr/bin/ffmpeg");

  const whichResult = spawnSync("which", ["-a", "ffmpeg"], {
    encoding: "utf8",
    timeout: 1000,
    killSignal: "SIGKILL",
  });

  if (whichResult.status === 0 && whichResult.stdout) {
    const discovered = whichResult.stdout
      .split("\n")
      .map((item) => item.trim())
      .filter(Boolean);

    for (const candidate of discovered) {
      if (candidate !== "/usr/local/bin/ffmpeg") {
        pushCandidate(candidate);
      }
    }
  }

  pushCandidate("ffmpeg");
  pushCandidate("/usr/local/bin/ffmpeg");

  for (const candidate of candidates) {
    if (candidate === "ffmpeg" || fs.existsSync(candidate)) {
      resolvedFfmpegBinary = candidate;
      return candidate;
    }
  }

  throw new Error(
    "No working ffmpeg binary was found. Install ffmpeg or set FFMPEG_PATH."
  );
}

function decodeAudioFile(filePath, sampleRate) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Audio file not found: ${filePath}`);
  }

  const ffmpegBinary = resolveFfmpegBinary();
  const result = spawnSync(
    ffmpegBinary,
    [
      "-v",
      "error",
      "-i",
      filePath,
      "-vn",
      "-ac",
      "1",
      "-ar",
      String(sampleRate),
      "-f",
      "f32le",
      "pipe:1",
    ],
    {
      encoding: null,
      maxBuffer: 1024 * 1024 * 512,
      timeout: 30000,
      killSignal: "SIGKILL",
    }
  );

  if (result.error) {
    throw new Error(`Failed to run ffmpeg: ${result.error.message}`);
  }

  if (result.status !== 0) {
    const stderr = result.stderr ? result.stderr.toString("utf8").trim() : "";
    throw new Error(stderr || "ffmpeg failed to decode the audio file.");
  }

  if (!result.stdout || result.stdout.length === 0) {
    throw new Error("ffmpeg returned an empty audio stream.");
  }

  return readF32LEBuffer(result.stdout);
}

function analyzeAudioFile(filePath, options = {}) {
  const sampleRate = parsePositiveNumber(
    options.sampleRate,
    DEFAULT_SAMPLE_RATE,
    "sample rate"
  );
  const minTempo = parsePositiveNumber(
    options.minTempo,
    DEFAULT_MIN_TEMPO,
    "min tempo"
  );
  const maxTempo = parsePositiveNumber(
    options.maxTempo,
    DEFAULT_MAX_TEMPO,
    "max tempo"
  );

  if (minTempo >= maxTempo) {
    throw new Error("min tempo must be lower than max tempo.");
  }

  const samples = decodeAudioFile(filePath, sampleRate);
  const monoProfile = buildMonoAudioProfile(samples, sampleRate);
  const primaryWindow = resolvePrimaryWindow(
    monoProfile.duration,
    parseOptionalNumber(options.offset, "offset"),
    parseOptionalNumber(options.duration, "duration")
  );
  const primaryProfile = buildOnsetEnvelope(monoProfile, primaryWindow);

  if (!primaryProfile) {
    throw new Error("Audio segment is too short or too quiet for reliable BPM detection.");
  }

  const primarySearch = collectTempoCandidates(
    primaryProfile.envelope,
    primaryProfile.frameRate,
    minTempo,
    maxTempo
  );

  if (primarySearch.candidates.length === 0) {
    throw new Error("No BPM candidates were detected for this audio file.");
  }

  let rankedCandidates = resolveOctaveAmbiguity(
    primarySearch.candidates,
    primaryProfile.envelope,
    primaryProfile.frameRate,
    primarySearch.autocorrelation,
    minTempo,
    maxTempo
  );

  if (rankedCandidates.length === 0) {
    rankedCandidates = primarySearch.candidates;
  }

  let consistency = 0.6;
  let windowPlan =
    Math.abs(primaryWindow.duration - monoProfile.duration) < 0.05
      ? "full"
      : "center-only";

  if (shouldRunSupplemental(rankedCandidates[0], rankedCandidates[1])) {
    const windows = buildSupplementalWindows(monoProfile.duration, primaryWindow);
    if (windows.length > 0) {
      const finalists = rankedCandidates.slice(0, 2).map((candidate) => ({ ...candidate }));
      let processedWindows = 0;

      for (const window of windows) {
        const profile = buildOnsetEnvelope(monoProfile, window);
        if (!profile) {
          continue;
        }

        processedWindows += 1;
        let bestIndex = 0;
        let bestScore = -Infinity;

        for (let index = 0; index < finalists.length; index += 1) {
          const rescored = scoreTempoCandidate(
            profile.envelope,
            profile.frameRate,
            finalists[index].tempo,
            computeAutocorrelation(profile.envelope, 2, profile.envelope.length - 2)
          );

          if (!rescored) {
            continue;
          }

          finalists[index].score += rescored.score;
          if (rescored.score > bestScore) {
            bestScore = rescored.score;
            bestIndex = index;
          }
        }

        finalists[bestIndex].support += 1;
      }

      rankedCandidates = [...finalists, ...rankedCandidates.slice(2)].sort(
        (left, right) => right.score - left.score
      );

      if (processedWindows > 0) {
        consistency = clamp(rankedCandidates[0].support / processedWindows, 0, 1);
        windowPlan = "center+supplemental";
      }
    }
  }

  let [bestCandidate, secondCandidate] = rankedCandidates;
  if (bestCandidate.tempo >= 150) {
    const halfCandidate = scoreTempoCandidate(
      primaryProfile.envelope,
      primaryProfile.frameRate,
      bestCandidate.tempo / 2,
      primarySearch.autocorrelation
    );

    if (
      halfCandidate &&
      halfCandidate.tempo >= 60 &&
      halfCandidate.tempo <= 110 &&
      halfCandidate.score >= bestCandidate.score * 0.72
    ) {
      secondCandidate = bestCandidate;
      bestCandidate = halfCandidate;
    }
  }

  if (bestCandidate.tempo < 69.5) {
    const tripletTempo = bestCandidate.tempo * 1.5;
    const tripletCandidate = scoreTempoCandidate(
      primaryProfile.envelope,
      primaryProfile.frameRate,
      tripletTempo,
      primarySearch.autocorrelation
    );

    if (
      tripletCandidate &&
      tripletTempo >= 90 &&
      tripletTempo <= 130 &&
      tripletCandidate.score >= bestCandidate.score * 0.88
    ) {
      secondCandidate = bestCandidate;
      bestCandidate = tripletCandidate;
    }
  }

  const tempo = bestCandidate.tempo;
  const bpm = Number(tempo.toFixed(1));
  const beatPeriod = 60 / Math.max(1e-6, tempo);
  const phaseSeconds = bestCandidate.phase / primaryProfile.frameRate;
  const offset =
    ((phaseSeconds + primaryWindow.offset) % beatPeriod + beatPeriod) % beatPeriod;

  return {
    source: "audio-file",
    filePath,
    bpm,
    confidence: calculateConfidence(bestCandidate, secondCandidate, consistency),
    durationSeconds: round(monoProfile.duration, 2),
    sampleRate,
    windowPlan,
    analysisWindow: {
      offsetSeconds: round(primaryWindow.offset, 2),
      durationSeconds: round(primaryWindow.duration, 2),
    },
    beatOffsetSeconds: round(offset, 3),
    candidateCount: rankedCandidates.length,
    minTempo,
    maxTempo,
  };
}

function loadFromFile(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const data = JSON.parse(raw);

  if (Array.isArray(data.intervals)) {
    return analyzeIntervals(parseNumberList(data.intervals.join(","), "intervals"));
  }

  if (Array.isArray(data.timestamps)) {
    return analyzeTimestamps(parseNumberList(data.timestamps.join(","), "timestamps"));
  }

  throw new Error('JSON file must contain either an "intervals" array or a "timestamps" array.');
}

function main() {
  const args = parseArgs(process.argv);

  if (args.help || Object.keys(args).length === 0) {
    console.log(
      [
        "Usage:",
        "  node scripts/tap-tempo.js --intervals 500,502,498,500",
        "  node scripts/tap-tempo.js --timestamps 0,500,1000,1500",
        "  node scripts/tap-tempo.js --audio-file ./song.mp3",
        "  node scripts/tap-tempo.js --file examples/sample-taps.json",
      ].join("\n")
    );
    process.exit(0);
  }

  let result;

  if (args.file) {
    result = loadFromFile(args.file);
  } else if (args["audio-file"] || args.audioFile) {
    result = analyzeAudioFile(args["audio-file"] || args.audioFile, {
      sampleRate: args["sample-rate"] || args.sampleRate,
      minTempo: args["min-tempo"] || args.minTempo,
      maxTempo: args["max-tempo"] || args.maxTempo,
      offset: args.offset,
      duration: args.duration,
    });
  } else if (args.intervals && args.timestamps) {
    throw new Error("Use either --intervals or --timestamps, not both.");
  } else if (args.intervals) {
    result = analyzeIntervals(parseNumberList(args.intervals, "intervals"));
  } else if (args.timestamps) {
    result = analyzeTimestamps(parseNumberList(args.timestamps, "timestamps"));
  } else {
    throw new Error(
      "Missing input. Use --intervals, --timestamps, --audio-file, or --file."
    );
  }

  console.log(JSON.stringify(result, null, 2));
}

try {
  main();
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
