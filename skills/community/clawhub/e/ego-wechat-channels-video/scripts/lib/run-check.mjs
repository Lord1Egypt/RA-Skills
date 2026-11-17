import {
  BASE,
  HOW_TO_LOGIN,
  HOW_TO_LOGIN_ZH,
  LOGIN_TIP,
  LOGIN_TIP_ZH,
  classifyLogin,
  strip,
} from "./pure.mjs";

export async function executeCheck(config, { browser }) {
  const summary = strip({
    skill: "wechat-channels-video",
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
      taskName: config.taskName || "wechat-channels-login-check",
      startUrl: BASE,
      keepBrowser: Boolean(config.keep),
    });
    summary.spaceId = session.spaceId;
    const detected = await session.detect();
    // One soft refresh if first paint is blank-ish
    if (!detected.platformChrome && !/login\.html/i.test(detected.url || "")) {
      await session.goto(BASE);
      Object.assign(detected, await session.detect());
    }
    const classified = classifyLogin({
      url: detected.url,
      title: detected.title,
      text: detected.text,
      signals: {
        platformChrome: detected.platformChrome,
        loggedInCookie: detected.loggedInCookie,
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
      summary.error = "WeChat Channels login required in Ego Lite";
      if (config.keep) {
        try {
          await session.handOff();
        } catch {
          // handOff optional
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
