// Generates the Apple OAuth client_secret JWT (valid up to 180 days).
//
// Requires an AuthKey_<KEY_ID>.p8 file in the working directory.
// Download the .p8 from: https://developer.apple.com/account/resources/authkeys/list
// (You can only download it once — store it safely.)
//
// Required env vars (from .env):
//   APPLE_TEAM_ID    — Membership: https://developer.apple.com/account
//   APPLE_KEY_ID     — Keys:       https://developer.apple.com/account/resources/authkeys/list
//   APPLE_CLIENT_ID  — Services:   https://developer.apple.com/account/resources/identifiers/serviceId
//
// Full setup walkthrough: ../references/auth.md

import { readFileSync } from "node:fs";

import dotenv from "dotenv";
import { importPKCS8, SignJWT } from "jose";

dotenv.config();

const teamId = process.env.APPLE_TEAM_ID;
const keyId = process.env.APPLE_KEY_ID;
const clientId = process.env.APPLE_CLIENT_ID;
const privateKeyPem = readFileSync(`./AuthKey_${keyId}.p8`, "utf8");

if (!teamId || !keyId || !clientId || !privateKeyPem) {
	throw new Error("Missing required environment variables");
}

const alg = "ES256";
const now = Math.floor(Date.now() / 1000);
const exp = now + 60 * 60 * 24 * 180; // 最长 180 天

const privateKey = await importPKCS8(privateKeyPem, alg);

const clientSecret = await new SignJWT({})
	.setProtectedHeader({ alg, kid: keyId })
	.setIssuer(teamId)
	.setIssuedAt(now)
	.setExpirationTime(exp)
	.setAudience("https://appleid.apple.com")
	.setSubject(clientId)
	.sign(privateKey);

console.log(`APPLE_CLIENT_SECRET:\n${clientSecret}`);
