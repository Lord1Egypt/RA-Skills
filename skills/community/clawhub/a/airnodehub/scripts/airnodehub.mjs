#!/usr/bin/env node

import { resolve as resolvePath } from 'node:path';
import { fileURLToPath } from 'node:url';
import { request as httpsRequest } from 'node:https';
import { lookup } from 'node:dns';
import { BlockList, isIP } from 'node:net';
import { encodePacked, isAddress, isHex, keccak256, toHex, verifyMessage } from 'viem';

const HUB_RESOLVE_URL = 'https://airnodehub.api3.org/resolve';
const TIMEOUT_MS = 20_000;
const HUB_CATALOGUE_URL = 'https://airnodehub.api3.org/llms.txt';
const fail = (message) => { throw new Error(message); };

const httpsUrl = (value, label = 'URL') => {
  let url;
  try { url = new URL(value); } catch { fail(`${label} is not a valid URL`); }
  if (url.protocol !== 'https:') fail(`${label} must use HTTPS`);
  if (url.username || url.password || url.hash || url.search || (url.port && url.port !== '443')) fail(`${label} contains unsupported URL components`);
  return url;
};

const blockedV4 = new BlockList();
for (const [ip, bits] of [['0.0.0.0',8],['10.0.0.0',8],['100.64.0.0',10],['127.0.0.0',8],['169.254.0.0',16],['172.16.0.0',12],['192.0.0.0',24],['192.0.2.0',24],['192.168.0.0',16],['198.18.0.0',15],['198.51.100.0',24],['203.0.113.0',24],['224.0.0.0',3]]) blockedV4.addSubnet(ip, bits);
const globalV6 = new BlockList();
globalV6.addSubnet('2000::', 3, 'ipv6');
const blockedV6 = new BlockList();
blockedV6.addSubnet('2001::', 23, 'ipv6');
blockedV6.addSubnet('2001:db8::', 32, 'ipv6');
blockedV6.addSubnet('2002::', 16, 'ipv6');
blockedV6.addSubnet('3fff::', 20, 'ipv6');
export const isPublicAddress = (ip) => isIP(ip) === 4 ? !blockedV4.check(ip) :
  isIP(ip) === 6 && globalV6.check(ip, 'ipv6') && !blockedV6.check(ip, 'ipv6');

export const safeFetch = (value, init = {}) => new Promise((resolve, reject) => {
  const url = httpsUrl(String(value));
  const hostname = url.hostname.replace(/^\[|\]$/g, '');
  if (isIP(hostname) && !isPublicAddress(hostname)) return reject(new Error('non-public destination refused'));
  const req = httpsRequest(url, {
    method: init.method ?? 'GET', headers: init.headers, signal: init.signal,
    lookup(host, options, callback) {
      lookup(host, { all: true }, (error, addresses) => {
        if (error) return callback(error);
        if (!addresses.length || addresses.some(({ address }) => !isPublicAddress(address)))
          return callback(new Error('non-public DNS destination refused'));
        if (options.all) callback(null, addresses);
        else callback(null, addresses[0].address, addresses[0].family);
      });
    },
  }, (res) => {
    if (res.statusCode >= 300 && res.statusCode < 400) {
      res.resume(); reject(new Error('redirect refused')); return;
    }
    const chunks = []; let size = 0;
    res.on('data', (chunk) => {
      size += chunk.length;
      if (size > 4 * 1024 * 1024) res.destroy(new Error('response exceeds 4 MiB'));
      else chunks.push(chunk);
    });
    res.on('error', reject);
    res.on('end', () => {
      const text = Buffer.concat(chunks).toString('utf8');
      resolve({ ok: res.statusCode >= 200 && res.statusCode < 300, status: res.statusCode,
        text: async () => text, json: async () => JSON.parse(text) });
    });
  });
  req.on('error', reject);
  req.setTimeout(TIMEOUT_MS, () => req.destroy(new Error('request timed out')));
  req.end(init.body);
});

const requireListedUrl = async (url, fetcher) => {
  const response = await fetcher(HUB_CATALOGUE_URL, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  if (!response.ok) fail('Hub catalogue unavailable');
  const text = await response.text();
  const urls = [...text.matchAll(/^[-] \[[^\]]+\]\((https:\/\/[^)]+)\):/gm)].map((match) => new URL(match[1]).href);
  if (!urls.includes(url.href)) fail('Airnode URL is absent from the current Hub catalogue');
};

const jsonResponse = async (response, label) => {
  if (!response.ok) fail(`${label} answered ${response.status}`);
  try { return await response.json(); } catch { fail(`${label} did not answer with JSON`); }
};

const object = (value, label) => {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) fail(`${label} is not an object`);
  return value;
};

const canonical = (value) => {
  if (Array.isArray(value)) return value.map(canonical);
  if (value === null || typeof value !== 'object') return value;
  return Object.entries(value).sort(([a], [b]) => a.localeCompare(b)).map(([key, nested]) => [key, canonical(nested)]);
};

export const deriveRequestHash = (operation, parameters, responseProjection) =>
  keccak256(toHex(JSON.stringify(responseProjection === undefined
    ? [operation, canonical(parameters)]
    : [operation, canonical(parameters), canonical(responseProjection)])));

const validAttestation = (value) =>
  typeof value === 'object' && value !== null && !Array.isArray(value) &&
  typeof value.airnode === 'string' && isAddress(value.airnode) &&
  typeof value.requestHash === 'string' && isHex(value.requestHash) && value.requestHash.length === 66 &&
  typeof value.timestamp === 'string' && /^\d+$/.test(value.timestamp) &&
  typeof value.signature === 'string' && isHex(value.signature) &&
  Object.hasOwn(value, 'data');

const attestationDigest = ({ requestHash, timestamp, data }) =>
  keccak256(encodePacked(
    ['bytes32', 'uint256', 'bytes'],
    [requestHash, BigInt(timestamp), toHex(typeof data === 'string' ? data : JSON.stringify(data))]
  ));

export const verifyExpectedAttestation = async (attestation, expected) =>
  attestation.airnode.toLowerCase() === expected.airnode.toLowerCase() &&
  attestation.requestHash === deriveRequestHash(expected.operation, expected.parameters, expected.responseProjection) &&
  verifyMessage({ address: attestation.airnode, message: { raw: attestationDigest(attestation) }, signature: attestation.signature });

export const resolveIntent = async (intent, options = {}) => {
  if (!intent.trim()) fail('intent is empty');
  const response = await (options.fetcher ?? safeFetch)(HUB_RESOLVE_URL, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ intent: intent.trim() }), signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  const result = object(await jsonResponse(response, 'Hub resolver'), 'Hub resolution');
  if (result.answerSource !== undefined && !['openRouter', 'localHeuristic'].includes(result.answerSource)) fail('Hub resolution has an invalid answerSource');
  if (!Array.isArray(result.candidates)) fail('Hub resolution has no candidates array');
  return result;
};

const operationsFrom = (document) => {
  const variants = document?.paths?.['/']?.post?.requestBody?.content?.['application/json']?.schema?.oneOf;
  if (!Array.isArray(variants)) fail('Airnode document has no POST operation variants');
  return variants.map((variant, index) => {
    const operation = variant?.properties?.operation?.const;
    const parameters = variant?.properties?.parameters;
    if (typeof operation !== 'string' || typeof parameters !== 'object' || parameters === null) fail(`Airnode operation variant ${index} is malformed`);
    return { operation, required: Array.isArray(parameters.required) ? parameters.required : [], properties: object(parameters.properties ?? {}, `parameters for ${operation}`) };
  });
};

export const inspectAirnode = async (airnodeUrl, options = {}) => {
  const url = httpsUrl(airnodeUrl, 'Airnode URL');
  const fetcher = options.fetcher ?? safeFetch;
  await requireListedUrl(url, fetcher);
  const response = await fetcher(url, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  const document = object(await jsonResponse(response, 'Airnode document'), 'Airnode document');
  const extension = object(document['x-airnode'], 'x-airnode');
  if (typeof extension.address !== 'string' || !isAddress(extension.address)) fail('Airnode document has no valid signer address');
  const payment = extension.payment === undefined ? undefined : object(extension.payment, 'x-airnode.payment');
  return {
    url: url.href, address: extension.address, operations: operationsFrom(document),
    payment: payment === undefined ? null : { network: payment.network, asset: payment.asset, prices: object(payment.prices ?? {}, 'x-airnode.payment.prices') },
  };
};

export const callFree = async (input, options = {}) => {
  const fetcher = options.fetcher ?? safeFetch;
  const inspected = await inspectAirnode(input.airnodeUrl, { fetcher });
  if (!isAddress(input.expectedAddress) || inspected.address.toLowerCase() !== input.expectedAddress.toLowerCase()) fail('live Airnode signer does not match the expected listing address');
  if (!inspected.operations.some((candidate) => candidate.operation === input.operation)) fail('operation is absent from the live Airnode document');
  const price = inspected.payment?.prices[input.operation];
  if (price !== undefined) return { state: 'needs-payment-authorisation', operation: input.operation, priceUsd: price, network: inspected.payment?.network, asset: inspected.payment?.asset };

  const response = await fetcher(httpsUrl(input.airnodeUrl, 'Airnode URL'), {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ operation: input.operation, parameters: input.parameters, ...(input.responseProjection === undefined ? {} : { responseProjection: input.responseProjection }) }), signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  const body = await jsonResponse(response, 'Airnode call');
  if (!validAttestation(body)) fail('Airnode response is not an attestation');
  if (!(await verifyExpectedAttestation(body, { airnode: input.expectedAddress, operation: input.operation, parameters: input.parameters, responseProjection: input.responseProjection }))) fail('Airnode attestation does not match the expected signer and exact request');
  return { state: 'verified', airnodeUrl: inspected.url, operation: input.operation, parameters: input.parameters, ...(input.responseProjection === undefined ? {} : { responseProjection: input.responseProjection }), data: body.data, attestation: body };
};

const parseParameters = (value) => {
  let parsed;
  try { parsed = JSON.parse(value); } catch { fail('parameters must be valid JSON'); }
  return object(parsed, 'parameters');
};

const main = async () => {
  const [command, ...args] = process.argv.slice(2);
  let result;
  if (command === 'resolve' && args.length === 1) result = await resolveIntent(args[0]);
  else if (command === 'inspect' && args.length === 1) result = await inspectAirnode(args[0]);
  else if (command === 'call-free' && [4, 5].includes(args.length)) result = await callFree({ airnodeUrl: args[0], operation: args[1], parameters: parseParameters(args[2]), expectedAddress: args[3], ...(args.length === 5 ? { responseProjection: parseParameters(args[4]) } : {}) });
  else fail("usage: airnodehub.mjs resolve '<intent>' | inspect '<url>' | call-free '<url>' '<operation>' '<parameters-json>' '<expected-address>' '[optional-projection-json]'");
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
};

if (process.argv[1] && fileURLToPath(import.meta.url) === resolvePath(process.argv[1])) {
  main().catch((error) => { process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`); process.exitCode = 1; });
}
