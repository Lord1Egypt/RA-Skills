#!/usr/bin/env node
import {
  createClient,
  exportKeystore,
  getDefaultKeystorePath,
  parseArgs,
  fmt,
  exitError,
  runMain,
  resolveNewPassword,
  jsonStringify,
} from "./_helpers.js";
import { writeFileSync } from "node:fs";
import { resolve as resolvePath } from "node:path";

const DELETE_FORCE_PHRASE = "force delete wallet";

await runMain(async () => {
  const client = await createClient();
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  switch (command) {
    case "create": {
      const existing = client.wallet.list();
      if (existing.length > 0) {
        exitError(`Wallet already exists (${existing[0].address}). Only one wallet is allowed per skill instance.`);
      }
      const password = await resolveNewPassword(args);
      const name = args._[1];
      const result = await client.wallet.create(password, name);
      console.log(jsonStringify({
        action: "create",
        address: result.address,
        keystoreFile: result.keystoreFile,
        keystoreDir: getDefaultKeystorePath(),
        name: name || null,
        passwordSaved: result.passwordSaved,
        ...(result.passwordSaveError
          ? { passwordSaveError: result.passwordSaveError }
          : {}),
      }, 2));
      break;
    }

    case "list": {
      const wallets = client.wallet.list();
      if (wallets.length === 0) {
        console.log(jsonStringify({ wallets: [] }, 2));
        break;
      }
      const results = [];
      for (const w of wallets) {
        const entry = { address: w.address, name: w.name || null };
        try {
          const bal = await client.query.getBalance(w.address);
          entry.bnb = fmt(bal.bnb);
          entry.atx = fmt(bal.atx);
          entry.usdt = fmt(bal.usdt);
        } catch (e) {
          entry.balanceError = e?.shortMessage || e?.message?.split("\n")[0] || String(e);
        }
        results.push(entry);
      }
      console.log(jsonStringify({ wallets: results }, 2));
      break;
    }

    case "export": {
      const address = args._[1];
      if (!address) {
        exitError("Usage: wallet.js export <address> [--out <file>]");
      }
      const { keystore, keystoreFile } = await exportKeystore(client, address, args);
      const outPath = typeof args.out === "string" ? resolvePath(args.out) : null;
      const json = jsonStringify(keystore, 2);
      if (outPath) {
        writeFileSync(outPath, json);
        console.log(jsonStringify({
          action: "export",
          address,
          format: "keystore-v3",
          source: keystoreFile,
          output: outPath,
        }, 2));
      } else {
        console.log(json);
      }
      break;
    }

    case "forget-password": {
      const address = args._[1];
      if (!address) exitError("Usage: wallet.js forget-password <address>");
      await client.wallet.forgetPassword(address);
      console.log(jsonStringify({ action: "forget-password", address, success: true }, 2));
      break;
    }

    case "has-password": {
      const address = args._[1];
      if (!address) exitError("Usage: wallet.js has-password <address>");
      const saved = await client.wallet.hasSavedPassword(address);
      console.log(jsonStringify({ address, hasSavedPassword: saved }, 2));
      break;
    }

    case "delete": {
      const address = args._[1];
      if (!address) {
        exitError("Usage: wallet.js delete <address> --backup-confirmed yes --force-phrase \"force delete wallet\"");
      }
      if (args["backup-confirmed"] !== "yes") {
        exitError("Refusing to delete wallet: export and back up the keystore first, then rerun with --backup-confirmed yes");
      }
      if (args["force-phrase"] !== DELETE_FORCE_PHRASE) {
        exitError("Refusing to delete wallet: rerun with --force-phrase \"force delete wallet\" after the user explicitly sends that exact phrase");
      }

      await client.wallet.delete(address);
      console.log(jsonStringify({
        action: "delete",
        address,
        deleted: true,
        backupConfirmed: true,
        forcePhrase: DELETE_FORCE_PHRASE,
      }, 2));
      break;
    }

    default:
      exitError("Usage: wallet.js <create|list|export|forget-password|has-password|delete> [args] [--password <pwd>]");
  }
});
