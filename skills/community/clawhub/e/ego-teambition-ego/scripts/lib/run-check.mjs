import {
  HOME_URL,
  HOW_TO_LOGIN,
  HOW_TO_LOGIN_ZH,
  LOGIN_TASK,
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  SKILL,
  classifyLogin,
  needsRepaint,
  strip,
} from "./pure.mjs";

export async function executeCheck(config, { browser }) {
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
    session = await browser.open({
      taskName: config.taskName || LOGIN_TASK,
      startUrl: HOME_URL,
      keepBrowser: Boolean(config.keep),
    });
    summary.spaceId = session.spaceId;
    const detected = await session.detect();
    if (needsRepaint(detected)) {
      await session.goto(HOME_URL);
      Object.assign(detected, await session.detect());
    }
    const classified = classifyLogin({
      url: detected.url,
      title: detected.title,
      text: detected.text,
      signals: {
        platformChrome: detected.platformChrome,
        loggedInCookie: detected.loggedInCookie,
        onLoginWall: detected.onLoginWall,
      },
    });
    Object.assign(summary, classified);
    summary.page = strip({ url: detected.url, title: detected.title });
    summary.signals = strip({
      platformChrome: detected.platformChrome,
      loggedInCookie: detected.loggedInCookie,
      on_login_page: classified.on_login_page,
    });

    if (classified.logged_in) {
      summary.ok = true;
      summary.login_required = false;
      summary.exitCode = 0;
    } else {
      summary.ok = false;
      summary.login_required = true;
      summary.exitCode = 2;
      summary.how_to_login = HOW_TO_LOGIN;
      summary.how_to_login_zh = HOW_TO_LOGIN_ZH;
      summary.error = "Teambition login required in Ego Lite";
      if (config.keep) {
        try {
          await session.handOff();
        } catch {
          // handOff is optional; the exit code is what agents must honor.
        }
      }
    }
  } catch (error) {
    summary.error = String(error.message || error);
    summary.exitCode = 1;
  } finally {
    if (session) {
      try {
        await session.finish();
      } catch (error) {
        summary.finish_error = String(error.message || error);
      }
    }
  }
  return summary;
}
