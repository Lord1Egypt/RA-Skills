import { classifyLogin, flowErrorBody, FRAME_URL, loginRequiredBody } from "./pure.mjs";

// Check the bilibili login state. Returns { summary, exitCode }.
export async function executeCheck(config, { browser }) {
  const keep = Boolean(config && config.keep);
  let space = null;
  try {
    space = await browser.open({
      taskName: (config && config.taskName) || "check bilibili login",
      startUrl: FRAME_URL,
      keepBrowser: keep,
    });
    const probe = await space.probe();
    const classified = classifyLogin({ url: probe.url, text: probe.text });
    if (!classified.logged_in) {
      const body = loginRequiredBody({ spaceId: space.spaceId, url: probe.url });
      if (keep) {
        try {
          await space.handOff();
        } catch {
          // exit code is the contract
        }
      } else {
        await space.finish();
      }
      return { summary: body, exitCode: 2 };
    }
    await space.finish();
    return {
      summary: {
        ok: true,
        login_required: false,
        exit_code: 0,
        spaceId: space.spaceId,
        url: probe.url,
        login_tip: "Ego 会话已登录 B 站创作中心。",
        how_to_login: "已登录,无需操作。",
        how_to_login_zh: "已登录,无需操作。",
      },
      exitCode: 0,
    };
  } catch (error) {
    const body = flowErrorBody(`检查登录失败: ${String((error && error.message) || error)}`, {
      spaceId: space ? space.spaceId : null,
    });
    try {
      if (space) await space.finish();
    } catch {
      // keep the original error
    }
    return { summary: { ...body, exit_code: 1 }, exitCode: 1 };
  }
}
