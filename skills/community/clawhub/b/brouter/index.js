const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');
const gpxParse = require('gpx-parse');

// All brouter logs go into a file next to this skill implementation so the
// location is stable regardless of the process working directory.
const LOG_PATH = path.resolve(__dirname, 'brouter.log');

function logEvent(event) {
  const payload = {
    ts: new Date().toISOString(),
    ...event,
  };

  fs.promises
    .appendFile(LOG_PATH, JSON.stringify(payload) + '\n', 'utf8')
    .catch(() => {
      // Ignore logging errors; they should not break the main flow.
    });
}

/**
 * Call the brouter.de webservice and persist the GPX response to disk.
 *
 * This is the programmatic entrypoint for the brouter-web skill.
 * It expects pre-computed coordinates in "lon,lat" form – use a separate
 * geocoding step to turn natural language locations into coordinates.
 *
 * @typedef {Object} BRouterOptions
 * @property {string} start         Required. Origin coordinates in "lon,lat" format.
 * @property {string} end           Required. Destination coordinates in "lon,lat" format.
 * @property {string} [profile]     Optional brouter profile (default: "trekking").
 * @property {string} [originLabel] Optional human-readable origin label used for filename slugs.
 * @property {string} [destinationLabel] Optional human-readable destination label used for filename slugs.
 * @property {string} [outputDir]   Directory where the GPX file should be written (default: "routes" subdirectory of process.cwd()).
 * @property {string} [fileName]    Optional explicit output filename. If omitted, a slug is generated.
 */

/**
 * Main handler for the brouter-web skill.
 *
 * @param {BRouterOptions} options
 * @returns {Promise<{
 *   gpxPath: string,
 *   lonlats: string,
 *   profile: string,
 *   summary: any,
 *   debug: {
 *     requestUrl: string,
 *     status: number,
 *     outputPath: string
 *   }
 * }>} Details about the generated GPX file and debug information.
 */
async function run(options = {}) {
  // Basic startup message for observability when the skill is invoked.
  // This prints to stdout so you can see calls immediately in the agent logs.
  // Note: full structured details are still written to brouter.log further below.
  // If options may contain sensitive data, adjust this log accordingly.
  console.log('[brouter] run() invoked with options:', options);

  const {
    start,
    end,
    profile = 'trekking',
    originLabel,
    destinationLabel,
    outputDir = path.resolve(process.cwd(), 'routes'),
    fileName,
  } = options;

  logEvent({
    type: 'brouter.run.start',
    options: { ...options },
  });
  if (!start || !end) {
    throw new Error('brouter: "start" and "end" coordinates are required ("<lon>,<lat>" format).');
  }

  const lonlats = `${start}|${end}`;
  const baseUrl = 'http://brouter.de/brouter';

  const params = new URLSearchParams();
  params.set('lonlats', lonlats);
  params.set('profile', profile);
  params.set('format', 'gpx');
  params.set('alternativeidx', '0');
  params.set('nogos', '');

  const requestUrl = `${baseUrl}?${params.toString()}`;

  let response;
  let status;
  try {
    response = await fetch(requestUrl);
    status = response.status;
  } catch (err) {
    // Network or fetch-layer error (no HTTP response). Always log call context
    logEvent({
      type: 'brouter.run.fetch_error',
      options: { ...options },
      request: {
        url: requestUrl,
        lonlats,
        profile,
      },
      response: null,
      error: {
        message: err.message,
        name: err.name,
      },
    });

    throw err;
  }

  if (!response.ok) {
    let body = '';
    try {
      body = await response.text();
    } catch (err) {
      // ignore
    }
    const error = new Error(`brouter: request ${requestUrl} failed with status ${status}`);
    error.status = status;
    error.body = body;

    // Log full call context on error: input options, request and response info.
    logEvent({
      type: 'brouter.run.error',
      options: { ...options },
      request: {
        url: requestUrl,
        lonlats,
        profile,
      },
      response: {
        status,
        body: body || null,
      },
      error: {
        message: error.message,
      },
    });

    throw error;
  }

  const gpxText = await response.text();

  const slugify = (value) =>
    String(value || '')
      .trim()
      .replace(/\s+/g, '_')
      .replace(/[^A-Za-z0-9_.-]/g, '') || null;

  const originSlug = slugify(originLabel || start);
  const destSlug = slugify(destinationLabel || end);

  const defaultFileName =
    originSlug && destSlug
      ? `bike-route-${originSlug}-${destSlug}.gpx`
      : 'bike-route.gpx';

  const finalFileName = fileName || defaultFileName;
  const outputPath = path.resolve(outputDir, finalFileName);

  await fs.promises.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.promises.writeFile(outputPath, gpxText, 'utf8');

  let summary = null;
  try {
    summary = await new Promise((resolve, reject) => {
      gpxParse.parseGpx(gpxText, (err, gpx) => {
        if (err) return reject(err);

        const result = {};

        if (gpx && Array.isArray(gpx.tracks) && gpx.tracks[0]) {
          const track = gpx.tracks[0];
          result.name = track.name || undefined;
          // Many consumers will post-process this further if needed.
        }

        resolve(result);
      });
    });
  } catch (_err) {
    // Parsing is best-effort; keep summary null on failure.
    summary = null;
  }

  const result = {
    gpxPath: outputPath,
    lonlats,
    profile,
    summary,
    attachment: {
      type: 'file',
      path: outputPath,
      name: finalFileName,
      mime: 'application/gpx+xml',
    },
    debug: {
      requestUrl,
      status,
      outputPath,
    },
  };

  // Log full call context on success: input parameters, the HTTP request, and the response metadata.
  logEvent({
    type: 'brouter.run.success',
    options: { ...options },
    request: {
      url: requestUrl,
      lonlats,
      profile,
    },
    response: {
      status,
      result: {
        gpxPath: result.gpxPath,
        lonlats: result.lonlats,
        profile: result.profile,
        summary: result.summary,
        debug: result.debug,
      },
    },
  });

  return result;
}

module.exports = run;
