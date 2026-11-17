#!/usr/bin/env node
/**
 * caniemail CLI — the skill surface.
 *
 * A thin argument parser over the shared core. Everything it prints is JSON on
 * stdout, because its only caller is an agent; errors go to stderr with a
 * non-zero exit.
 *
 * Usage:
 *   caniemail.mjs lint    --clients outlook.windows,gmail.* [--html FILE] [--css FILE]
 *   caniemail.mjs check   <feature-slug> --clients outlook.*
 *   caniemail.mjs search  <query> [--category css] [--limit 10]
 *   caniemail.mjs clients
 */

import { readFile } from 'node:fs/promises';
import { argv, exit, stdin, stdout } from 'node:process';
import { parseArgs } from 'node:util';

import {
  checkFeatureSupport,
  lintEmail,
  listClients,
  loadDataset,
  searchFeatures,
} from './caniemail-core.mjs';

const USAGE = `caniemail — email client compatibility for HTML and CSS

  lint     --clients <globs> [--html FILE] [--css FILE] [--no-untested]
           Lint markup and report only what breaks. Reads stdin as HTML if
           neither --html nor --css is given.

  check    <feature-slug> --clients <globs> [--version <v>]
           Per-client verdict for one feature.

  search   <query> [--category html|css|image|others] [--limit N]
           Find feature slugs by keyword. Start here; slugs are not guessable.

  clients  List every client identifier.

Options:
  --clients   Comma-separated "family.platform" globs: outlook.windows,
              gmail.*, *.ios, or * for all.
  --offline   Skip the network and use the bundled dataset.
  --refresh   Force a fresh fetch, ignoring the cache.
`;

/**
 * Every option the commands read. `node:util`'s `parseArgs` rejects anything
 * not listed here, so a typo such as `--limt 3` is an error rather than a flag
 * nobody reads and a `3` taken for its value.
 */
const OPTIONS = /** @type {const} */ ({
  help: { type: 'boolean' },
  offline: { type: 'boolean' },
  refresh: { type: 'boolean' },
  'no-untested': { type: 'boolean' },
  clients: { type: 'string' },
  html: { type: 'string' },
  css: { type: 'string' },
  version: { type: 'string' },
  category: { type: 'string' },
  limit: { type: 'string' },
});

/** @typedef {ReturnType<typeof parseCommandLine>['flags']} Flags */

/**
 * @param {string[]} args
 */
function parseCommandLine(args) {
  try {
    const { values, positionals } = parseArgs({
      args,
      options: OPTIONS,
      allowPositionals: true,
      strict: true,
    });
    return { positional: positionals, flags: values };
  } catch (error) {
    if (!(error instanceof Error)) throw error;
    throw new Error(rephrase(error), { cause: error });
  }
}

/**
 * Node's messages for a bad command line are written for a script author and
 * suggest `--name=-XYZ` and `--` escapes. Say what is wrong in this CLI's terms
 * instead, keeping Node's text for anything not recognised here.
 *
 * `--clients --offline` lands in the second case: a value option followed by
 * another option has no value, rather than a client called "--offline" and an
 * offline run that went to the network.
 *
 * @param {Error} error
 */
function rephrase(error) {
  const code = 'code' in error ? error.code : undefined;
  const option = /'(-[^' ]+)/.exec(error.message)?.[1];
  if (!option) return error.message;
  if (code === 'ERR_PARSE_ARGS_UNKNOWN_OPTION') {
    return `Unknown option ${option}. Run with --help for the options.`;
  }
  if (code === 'ERR_PARSE_ARGS_INVALID_OPTION_VALUE') {
    return error.message.includes('does not take')
      ? `${option} takes no value.`
      : `${option} needs a value.`;
  }
  return error.message;
}

/** @param {Flags} flags */
function clientsFrom(flags) {
  if (!flags.clients) {
    throw new Error('--clients is required, e.g. --clients outlook.windows,gmail.*');
  }
  return flags.clients
    .split(',')
    .map((c) => c.trim())
    .filter(Boolean);
}

async function readStdin() {
  if (stdin.isTTY) return '';
  let text = '';
  for await (const chunk of stdin) text += chunk;
  return text;
}

/**
 * Compact when piped, indented when a person is looking.
 *
 * The caller is normally an agent reading stdout into its context, where
 * indentation is pure cost — on a lint against all 48 clients it was 16KB of
 * whitespace, about 4k tokens. At a terminal it is worth the bytes, and stdout
 * being a TTY is exactly the signal that distinguishes the two.
 *
 * @param {unknown} value
 */
function print(value) {
  process.stdout.write(`${JSON.stringify(value, null, stdout.isTTY ? 2 : 0)}\n`);
}

async function main() {
  const { positional, flags } = parseCommandLine(argv.slice(2));
  const [command, ...rest] = positional;

  if (!command || flags.help) {
    process.stdout.write(USAGE);
    return;
  }

  const dataset = await loadDataset({
    offline: Boolean(flags.offline),
    maxAgeMs: flags.refresh ? 0 : undefined,
  });

  switch (command) {
    case 'lint': {
      const html = flags.html ? await readFile(flags.html, 'utf8') : undefined;
      const css = flags.css ? await readFile(flags.css, 'utf8') : undefined;
      const fallback = html || css ? undefined : await readStdin();
      print(
        lintEmail(dataset, {
          html: html ?? fallback,
          css,
          clients: clientsFrom(flags),
          includeUntested: !flags['no-untested'],
        }),
      );
      return;
    }

    case 'check': {
      const [slug] = rest;
      if (!slug) throw new Error('check requires a feature slug, e.g. check css-display-flex');
      print(checkFeatureSupport(dataset, slug, clientsFrom(flags), { version: flags.version }));
      return;
    }

    case 'search': {
      const query = rest.join(' ');
      if (!query) throw new Error('search requires a query, e.g. search "rounded corners"');
      print(
        searchFeatures(dataset, query, {
          category: flags.category,
          limit: flags.limit ? Number(flags.limit) : undefined,
        }),
      );
      return;
    }

    case 'clients': {
      print(listClients(dataset));
      return;
    }

    default:
      throw new Error(`Unknown command "${command}".\n\n${USAGE}`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  exit(1);
});
