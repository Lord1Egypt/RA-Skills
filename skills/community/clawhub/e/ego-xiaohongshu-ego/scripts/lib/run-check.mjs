import {
  CREATOR_HOME,
  HOW_TO_LOGIN,
  HOW_TO_LOGIN_ZH,
  LOGIN_TASK,
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  SKILL,
  accountGate,
  classifyLogin,
  needsRepaint,
  onCreator,
  strip,
} from "./pure.mjs";

export async function readGate(session, expectAccount, { allowRepaint = true } = {}) {
  let detected = await session.detect();
  if (allowRepaint && needsRepaint(detected)) {
    const again = onCreator(detected.url) ? detected.url : CREATOR_HOME;
    await session.goto(again);
    detected = await session.detect();
  }
  const classified = classifyLogin(detected);
  const account = accountGate({
    nickname: detected.nickname || classified.nickname || "",
    expected: expectAccount,
    text: detected.text,
    loggedIn: classified.logged_in,
  });
  return {
    ...classified,
    ...account,
    nickname: account.nickname || classified.nickname || detected.nickname || "",
    text: detected.text || "",
    evaluateError: detected.evaluateError || "",
  };
}

function loginRequiredSummary(gate) {
  return strip({
    ok: false,
    logged_in: false,
    login_required: true,
    exitCode: 2,
    on_login_page: gate.on_login_page,
    url: gate.url,
    title: gate.title,
    error: gate.evaluateError ? String(gate.evaluateError) : "Xiaohongshu creator login required in Ego Lite",
    how_to_login: HOW_TO_LOGIN,
    how_to_login_zh: HOW_TO_LOGIN_ZH,
  });
}

function mismatchSummary(gate) {
  return strip({
    ok: false,
    logged_in: true,
    login_required: false,
    account_mismatch: true,
    exitCode: 2,
    nickname: gate.nickname || undefined,
    error: gate.error || "account mismatch",
    how_to_login: HOW_TO_LOGIN,
    how_to_login_zh: HOW_TO_LOGIN_ZH,
  });
}

async function handOffIfKept(session, keep) {
  if (!keep) return;
  try {
    await session.handOff();
  } catch {
    // handOff is optional; the exit code is what agents must honor.
  }
}

export async function executeCheck(config = {}, { browser } = {}) {
  const summary = strip({
    skill: SKILL,
    command: "check-login",
    ok: false,
    logged_in: false,
    login_required: true,
    exitCode: 2,
    login_tip: LOGIN_TIP,
    login_tip_zh: LOGIN_TIP_ZH,
    spaceId: undefined,
    page: undefined,
    error: null,
  });
  let session;
  try {
    if (!browser || typeof browser.open !== "function") throw new Error("browser is required");
    session = await browser.open({
      taskName: config.taskName || LOGIN_TASK,
      startUrl: CREATOR_HOME,
      keepBrowser: Boolean(config.keep),
    });
    summary.spaceId = session.spaceId;
    const gate = await readGate(session, config.expectAccount);
    summary.page = strip({ url: gate.url, title: gate.title });
    summary.nickname = gate.nickname || undefined;
    if (gate.evaluateError) {
      summary.ok = false;
      summary.logged_in = false;
      summary.exitCode = 1;
      summary.error = gate.evaluateError;
    } else if (!gate.logged_in) {
      Object.assign(summary, loginRequiredSummary(gate));
      await handOffIfKept(session, config.keep);
    } else if (!gate.ok) {
      Object.assign(summary, mismatchSummary(gate));
    } else {
      summary.ok = true;
      summary.logged_in = true;
      summary.login_required = false;
      summary.exitCode = 0;
      summary.error = undefined;
      summary.account_mismatch = false;
    }
  } catch (error) {
    summary.error = String(error && error.message ? error.message : error);
    summary.exitCode = 1;
  } finally {
    if (session) {
      try {
        await session.finish();
      } catch (error) {
        summary.finish_error = String(error && error.message ? error.message : error);
      }
    }
  }
  return summary;
}

export { loginRequiredSummary, mismatchSummary };
