#!/usr/bin/env node

/**
 * fb-post.js — Publish to a Facebook Page via Graph API
 *
 * Usage:
 *   node fb-post.js --type text --message "Hello world"
 *   node fb-post.js --type image --message "Photo" --image-url "https://..."
 *   node fb-post.js --type image --message "Photo" --image-file ./pic.jpg
 *   node fb-post.js --type text --message "Post" --comment-link "https://example.com"
 *   node fb-post.js --type text --message "Post" --schedule "2025-12-25T10:00:00+0800"
 *
 * Env vars required:
 *   LONG_META_page_TOKEN  — Long-lived Page Access Token
 *   META_PAGE_ID          — Facebook Page ID
 *   META_APP_SECRET       — Meta App Secret (for appsecret_proof)
 */

import { createHmac } from "node:crypto";
import { readFile } from "node:fs/promises";
import { basename } from "node:path";

// --- Config ---

const PAGE_TOKEN = process.env.LONG_META_page_TOKEN;
const PAGE_ID = process.env.META_PAGE_ID;
const APP_SECRET = process.env.META_APP_SECRET;
const API_VERSION = "v21.0";
const BASE = `https://graph.facebook.com/${API_VERSION}`;

if (!PAGE_TOKEN || !PAGE_ID || !APP_SECRET) {
  console.error(
    "Error: missing env vars. Required:\n" +
      "  LONG_META_page_TOKEN\n" +
      "  META_PAGE_ID\n" +
      "  META_APP_SECRET"
  );
  process.exit(1);
}

// --- Helpers ---

function proof() {
  return createHmac("sha256", APP_SECRET).update(PAGE_TOKEN).digest("hex");
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const val = argv[i + 1];
      if (val && !val.startsWith("--")) {
        args[key] = val;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

async function api(endpoint, body, formData = false) {
  const url = `${BASE}${endpoint}`;
  const opts = { method: "POST" };

  if (formData) {
    body.append("access_token", PAGE_TOKEN);
    body.append("appsecret_proof", proof());
    opts.body = body;
  } else {
    const p = new URLSearchParams(body);
    p.append("access_token", PAGE_TOKEN);
    p.append("appsecret_proof", proof());
    opts.body = p.toString();
    opts.headers = { "Content-Type": "application/x-www-form-urlencoded" };
  }

  const res = await fetch(url, opts);
  const data = await res.json();

  if (!res.ok) {
    throw new Error(
      `Graph API ${res.status}: ${data?.error?.message || JSON.stringify(data)}`
    );
  }
  return data;
}

// --- Post functions ---

async function postText(msg, schedule) {
  const body = { message: msg };
  if (schedule) {
    body.published = "false";
    body.scheduled_publish_time = String(
      Math.floor(new Date(schedule).getTime() / 1000)
    );
  }
  const r = await api(`/${PAGE_ID}/feed`, body);
  return { postId: r.id, type: "text" };
}

async function postImageUrl(msg, url, schedule) {
  const body = { message: msg, url };
  if (schedule) {
    body.published = "false";
    body.scheduled_publish_time = String(
      Math.floor(new Date(schedule).getTime() / 1000)
    );
  }
  const r = await api(`/${PAGE_ID}/photos`, body);
  return { postId: r.post_id || r.id, photoId: r.id, type: "image-url" };
}

async function postImageFile(msg, path, schedule) {
  const buf = await readFile(path);
  const fd = new FormData();
  fd.append("message", msg);
  fd.append("source", new Blob([buf]), basename(path));
  if (schedule) {
    fd.append("published", "false");
    fd.append(
      "scheduled_publish_time",
      String(Math.floor(new Date(schedule).getTime() / 1000))
    );
  }
  const r = await api(`/${PAGE_ID}/photos`, fd, true);
  return { postId: r.post_id || r.id, photoId: r.id, type: "image-file" };
}

async function comment(postId, text) {
  const r = await api(`/${postId}/comments`, { message: text });
  return { commentId: r.id };
}

// --- Main ---

async function main() {
  const a = parseArgs(process.argv);
  const type = a.type || "text";
  const msg = a.message;

  if (!msg) {
    console.error("Error: --message is required.");
    process.exit(1);
  }

  console.log(`Publishing ${type} post to page ${PAGE_ID}...`);
  if (a.schedule) console.log(`Scheduled: ${a.schedule}`);

  let result;
  try {
    if (type === "text") {
      result = await postText(msg, a.schedule);
    } else if (type === "image") {
      if (a["image-file"]) {
        result = await postImageFile(msg, a["image-file"], a.schedule);
      } else if (a["image-url"]) {
        result = await postImageUrl(msg, a["image-url"], a.schedule);
      } else {
        console.error("Error: image post needs --image-url or --image-file");
        process.exit(1);
      }
    } else {
      console.error(`Error: unknown type "${type}". Use "text" or "image".`);
      process.exit(1);
    }

    console.log(`Done. Post ID: ${result.postId}`);
    if (result.photoId) console.log(`Photo ID: ${result.photoId}`);

    if (a["comment-link"] && result.postId) {
      let target = result.postId;
      if (!target.includes("_")) target = `${PAGE_ID}_${target}`;
      console.log("Adding link as first comment...");
      const c = await comment(target, a["comment-link"]);
      console.log(`Comment ID: ${c.commentId}`);
    }

    console.log(
      JSON.stringify(
        {
          success: true,
          ...result,
          scheduled: a.schedule || null,
          commentLink: a["comment-link"] || null,
        },
        null,
        2
      )
    );
  } catch (err) {
    console.error(`Error: ${err.message}`);
    if (err.message.includes("OAuth")) {
      console.error("Token may be expired. Re-generate your Page Access Token.");
    }
    process.exit(1);
  }
}

main();
