import fs from "node:fs/promises";

import {
  apiPath,
  collectPositionals,
  exitWithError,
  findAllOptions,
  findOption,
  hasFlag,
  printJson,
  readCountOption,
  requireCommandValue,
  sanitizeForOutput,
} from "./utils.js";
import {
  handleAuthAppsCommand,
  handleAuthProfilesCommand,
  handleConfigCommand,
  resolveCookieArg,
  resolveAppState,
  saveConfig,
} from "./config.js";
import { performRequest } from "./request.js";

const ARTICLE_PUBLISH_MD_USAGE = "Usage: apitweet article publish-md <file.md> --title <title> [--cover-image <url_or_path>] [--visibility Public|Followers|Mentioned]";
const ARTICLE_ID_PLACEHOLDER = "{article_id_from_step_1}";
const ARTICLE_VISIBILITIES = new Set(["Public", "Followers", "Mentioned"]);

function tweetActionBody(args, state, config) {
  const proxy = findOption(args, "--proxy");
  return {
    cookie: resolveCookieArg(args, state, config),
    ...(proxy ? { proxy } : {}),
  };
}

function buildTweetBody(args, state, config) {
  const text = requireCommandValue(findOption(args, "--text"), "Usage: apitweet tweet create --text <content> [--media-url <url>] [--reply-to <tweet_id>]");
  const mediaUrls = findAllOptions(args, "--media-url");
  const proxy = findOption(args, "--proxy");
  const delegatedAccount = findOption(args, "--delegated-account");
  const communityName = findOption(args, "--community");
  const schedule = findOption(args, "--schedule");
  const replyTweetId = findOption(args, "--reply-to");

  return {
    tweet_content: text,
    cookie: resolveCookieArg(args, state, config),
    ...(mediaUrls[0] ? { media_url: mediaUrls[0] } : {}),
    ...(delegatedAccount ? { delegated_account_username: delegatedAccount } : {}),
    ...(communityName ? { community_name: communityName } : {}),
    ...(schedule ? { schedule } : {}),
    ...(replyTweetId ? { reply_tweet_id: replyTweetId } : {}),
    ...(proxy ? { proxy } : {}),
  };
}

async function handleAuthCookieCommand(state, config, args) {
  const authToken = requireCommandValue(findOption(args, "--auth-token"), "Usage: apitweet auth cookie --auth-token <token> [--save-as <profile>] [--ct0 <value>]");
  const saveAs = findOption(args, "--save-as");
  const response = await performRequest(state, config, {
    method: "GET",
    path: `/twitter/${encodeURIComponent(authToken)}/cookie`,
    silent: Boolean(saveAs),
  });

  if (state.dryRun || !saveAs) {
    return;
  }

  const cookie = typeof response.data?.data === "string" ? response.data.data : "";
  if (!cookie) {
    exitWithError("Cookie response did not contain a usable cookie string.");
  }

  const ct0 = findOption(args, "--ct0");
  config.profiles[saveAs] = {
    cookie,
    authToken,
    ...(ct0 ? { ct0 } : {}),
  };
  if (!config.currentProfile || hasFlag(args, "--use")) {
    config.currentProfile = saveAs;
  }
  await saveConfig(state.configDir, config);

  console.log(JSON.stringify({
    saved: saveAs,
    currentProfile: config.currentProfile,
    profile: {
      cookie: cookie ? `${cookie.slice(0, 4)}...${cookie.slice(-4)}` : "",
      authToken: authToken ? `${authToken.slice(0, 4)}...${authToken.slice(-4)}` : "",
      ct0: ct0 ? `${ct0.slice(0, 4)}...${ct0.slice(-4)}` : "",
    },
  }, null, 2));
}

async function handleAuthCommand(state, config, args) {
  const area = args[1];
  if (area === "apps") {
    await handleAuthAppsCommand(state, config, args);
    return;
  }
  if (area === "profiles") {
    await handleAuthProfilesCommand(state, config, args);
    return;
  }
  if (area === "cookie") {
    await handleAuthCookieCommand(state, config, args);
    return;
  }

  exitWithError("Unknown auth command.", "Use: auth apps | auth profiles | auth cookie");
}

async function handleUsersCommand(state, config, args) {
  const usernames = collectPositionals(args, 1);
  if (usernames.length === 0) {
    exitWithError("Usage: apitweet users <username...>");
  }

  await performRequest(state, config, {
    method: "POST",
    path: "/twitter/users",
    body: usernames,
  });
}

async function handleAboutCommand(state, config, args) {
  const screenName = requireCommandValue(args[1], "Usage: apitweet about <screen_name>");
  await performRequest(state, config, {
    method: "GET",
    path: `/twitter/${encodeURIComponent(screenName)}/about`,
  });
}

async function handleSearchCommand(state, config, args) {
  const scope = args[1];

  if (scope === "tweets") {
    const terms = collectPositionals(args, 2, ["--count", "--sort"]);
    if (terms.length === 0) {
      exitWithError("Usage: apitweet search tweets <term...> [--count <n>] [--sort Latest|Top]");
    }

    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/advanced_search",
      body: {
        searchTerms: terms,
        maxItems: readCountOption(args, 20),
        sortBy: findOption(args, "--sort") || "Latest",
      },
    });
    return;
  }

  if (scope === "users") {
    const keyword = requireCommandValue(args[2], "Usage: apitweet search users <keyword> [--count <n>]");
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/search-user/${encodeURIComponent(keyword)}/${readCountOption(args, 20)}`,
    });
    return;
  }

  exitWithError("Unknown search command.", "Use: search tweets | search users");
}

async function handleArticleCommand(state, config, args) {
  const action = args[1];
  if (action === "markdown") {
    const tweetId = requireCommandValue(args[2], "Usage: apitweet article markdown <tweet_id>");
    await performRequest(state, config, {
      method: "GET",
      path: `/x/article/${encodeURIComponent(tweetId)}/markdown`,
    });
    return;
  }

  if (action === "lookup") {
    const tweetIds = collectPositionals(args, 2);
    if (tweetIds.length === 0) {
      exitWithError("Usage: apitweet article lookup <tweet_id...>");
    }
    await performRequest(state, config, {
      method: "POST",
      path: "/x/article",
      body: tweetIds,
    });
    return;
  }

  if (action === "publish-md") {
    await handleArticlePublishMdCommand(state, config, args);
    return;
  }

  exitWithError("Unknown article command.", "Use: article markdown | article lookup | article publish-md");
}

function articlePublishMdRequests(articleId, data) {
  const { cookie, coverImage, markdown, title, visibility } = data;
  const articlePath = `/x/articles/${articleId}`;
  const requests = [
    {
      name: "create_draft",
      method: "POST",
      path: "/x/articles/draft",
      body: { cookie },
    },
  ];

  if (coverImage) {
    requests.push({
      name: "set_cover",
      method: "PUT",
      path: `${articlePath}/cover`,
      body: {
        cookie,
        cover_image: coverImage,
      },
    });
  }

  requests.push(
    {
      name: "set_title",
      method: "PUT",
      path: `${articlePath}/title`,
      body: {
        cookie,
        title,
      },
    },
    {
      name: "set_content",
      method: "PUT",
      path: `${articlePath}/content`,
      body: {
        cookie,
        markdown,
      },
    },
    {
      name: "publish",
      method: "POST",
      path: `${articlePath}/publish`,
      body: {
        cookie,
        visibility,
      },
    },
  );

  return requests;
}

function buildDryRunPreview(state, config, request) {
  const appState = resolveAppState(state, config);
  const target = apiPath(request.path);
  const url = /^https?:\/\//i.test(target) ? target : `${appState.baseUrl}${target}`;
  const headers = {
    Accept: "application/json",
    ...state.headers,
    ...request.headers,
  };

  if (appState.apiKey) {
    headers.Authorization = `Bearer ${appState.apiKey}`;
  }

  return sanitizeForOutput({
    name: request.name,
    method: request.method,
    url,
    headers,
    ...(request.body !== undefined ? { body: request.body } : {}),
  });
}

function articleIdFromDraftResponse(response) {
  const articleId = response.data?.data?.article_id;
  if (!articleId) {
    exitWithError("Draft response did not contain article_id.");
  }
  return articleId;
}

async function readMarkdownFile(filePath) {
  try {
    return await fs.readFile(filePath, "utf8");
  } catch (error) {
    exitWithError("Failed to read markdown file.", error.message);
  }
}

async function handleArticlePublishMdCommand(state, config, args) {
  const filePath = requireCommandValue(args[2], ARTICLE_PUBLISH_MD_USAGE);
  const title = requireCommandValue(findOption(args, "--title"), ARTICLE_PUBLISH_MD_USAGE);
  const coverImage = findOption(args, "--cover-image");
  const visibility = findOption(args, "--visibility") || "Public";

  if (!ARTICLE_VISIBILITIES.has(visibility)) {
    exitWithError(`Invalid --visibility value: ${visibility}`, "Use: Public | Followers | Mentioned");
  }

  const markdown = await readMarkdownFile(filePath);
  const cookie = resolveCookieArg(args, state, config);
  const data = {
    cookie,
    coverImage,
    markdown,
    title,
    visibility,
  };

  if (state.dryRun) {
    printJson({
      articleId: ARTICLE_ID_PLACEHOLDER,
      steps: articlePublishMdRequests(ARTICLE_ID_PLACEHOLDER, data).map((request) => buildDryRunPreview(state, config, request)),
    });
    return;
  }

  const draftRequest = articlePublishMdRequests("", data)[0];
  const draftResponse = await performRequest(state, config, {
    ...draftRequest,
    silent: true,
  });
  const articleId = articleIdFromDraftResponse(draftResponse);
  const remainingRequests = articlePublishMdRequests(encodeURIComponent(articleId), data).slice(1);

  for (const [index, request] of remainingRequests.entries()) {
    await performRequest(state, config, {
      ...request,
      silent: index < remainingRequests.length - 1,
    });
  }
}

async function handleDmCommand(state, config, args) {
  const action = args[1];
  const proxy = findOption(args, "--proxy");

  if (action === "history") {
    const username = requireCommandValue(args[2], "Usage: apitweet dm history <username> [--max-id <id>]");
    const maxId = findOption(args, "--max-id");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/dm-history",
      body: {
        username,
        cookie: resolveCookieArg(args, state, config),
        ...(maxId ? { max_id: maxId } : {}),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  if (action === "send") {
    const username = requireCommandValue(args[2], "Usage: apitweet dm send <username> --text <content> [--media-url <url>] [--reply-to <id>]");
    const text = requireCommandValue(findOption(args, "--text"), "Usage: apitweet dm send <username> --text <content> [--media-url <url>] [--reply-to <id>]");
    const mediaUrl = findOption(args, "--media-url");
    const replyTo = findOption(args, "--reply-to");

    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/send-dm",
      body: {
        username,
        msg: text,
        cookie: resolveCookieArg(args, state, config),
        ...(mediaUrl ? { media: mediaUrl } : {}),
        ...(replyTo ? { reply_to: replyTo } : {}),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  exitWithError("Unknown dm command.", "Use: dm history | dm send");
}

async function handleFollowersCommand(state, config, args) {
  const screenName = requireCommandValue(args[1], "Usage: apitweet followers <screen_name> [--count <n>]");
  await performRequest(state, config, {
    method: "GET",
    path: `/twitter/followers/${encodeURIComponent(screenName)}/${readCountOption(args, 200)}`,
  });
}

async function handleFollowingCommand(state, config, args) {
  const screenName = requireCommandValue(args[1], "Usage: apitweet following <screen_name> [--count <n>]");
  await performRequest(state, config, {
    method: "GET",
    path: `/twitter/following/${encodeURIComponent(screenName)}/${readCountOption(args, 200)}`,
  });
}

async function handleTimelineCommand(state, config, args) {
  const action = args[1];
  if (action === "user") {
    const screenName = requireCommandValue(args[2], "Usage: apitweet timeline user <screen_name> [--cursor <token>] [--count <n>]");
    const cursor = findOption(args, "--cursor");
    const count = readCountOption(args, 20);

    await performRequest(state, config, {
      method: "POST",
      path: `/twitter/${encodeURIComponent(screenName)}/timeline/page`,
      body: {
        ...(cursor ? { next_cursor: cursor } : {}),
        count,
      },
    });
    return;
  }

  exitWithError("Unknown timeline command.", "Use: timeline user");
}

async function handleTrendingCommand(state, config, args) {
  const action = args[1];

  if (action === "tweets") {
    const country = requireCommandValue(findOption(args, "--country"), "Usage: apitweet trending tweets --country <country> [--topic <topic>] [--content <content>] [--count <n>]");
    const topic = findOption(args, "--topic");
    const content = findOption(args, "--content");
    const count = readCountOption(args, 20);
    const params = new URLSearchParams({ country });

    if (topic) {
      params.set("topic", topic);
    }
    if (content) {
      params.set("content", content);
    }
    params.set("count", String(count));

    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/global-trending/tweets?${params.toString()}`,
    });
    return;
  }

  exitWithError("Unknown trending command.", "Use: trending tweets");
}

async function handleProfileCommand(state, config, args) {
  const action = args[1];
  if (action === "update") {
    const name = findOption(args, "--name");
    const description = findOption(args, "--description");
    const location = findOption(args, "--location");
    const website = findOption(args, "--website");
    const profileImage = findOption(args, "--image-url");
    const profileBanner = findOption(args, "--banner-url");
    const proxy = findOption(args, "--proxy");

    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/profile",
      body: {
        cookie: resolveCookieArg(args, state, config),
        ...(name ? { name } : {}),
        ...(description ? { description } : {}),
        ...(location ? { location } : {}),
        ...(website ? { website } : {}),
        ...(profileImage ? { profile_image: profileImage } : {}),
        ...(profileBanner ? { profile_banner: profileBanner } : {}),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  exitWithError("Unknown profile command.", "Use: profile update");
}

async function handleListCommand(state, config, args) {
  const action = args[1];

  if (action === "search") {
    const query = requireCommandValue(findOption(args, "--query"), "Usage: apitweet list search --query <text> [--count <n>]");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/list/search",
      body: {
        query,
        target_count: readCountOption(args, 20),
      },
    });
    return;
  }

  if (action === "create") {
    const listName = requireCommandValue(findOption(args, "--name"), "Usage: apitweet list create --name <name> --description <text> [--private]");
    const listDescription = requireCommandValue(findOption(args, "--description"), "Usage: apitweet list create --name <name> --description <text> [--private]");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/list/create",
      body: {
        cookie: resolveCookieArg(args, state, config),
        list_name: listName,
        list_description: listDescription,
        is_private: hasFlag(args, "--private"),
      },
    });
    return;
  }

  if (action === "members") {
    const listId = requireCommandValue(args[2], "Usage: apitweet list members <list_id> [--count <n>]");
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/list/${encodeURIComponent(listId)}/members/${readCountOption(args, 100)}`,
    });
    return;
  }

  if (action === "subscribers") {
    const listId = requireCommandValue(args[2], "Usage: apitweet list subscribers <list_id> [--count <n>]");
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/list/${encodeURIComponent(listId)}/subscribers/${readCountOption(args, 100)}`,
    });
    return;
  }

  exitWithError("Unknown list command.", "Use: list search | list create | list members | list subscribers");
}

async function handleTweetCommand(state, config, args) {
  const action = args[1];

  if (action === "create") {
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/tweets/create",
      body: buildTweetBody(args, state, config),
    });
    return;
  }

  if (action === "quote") {
    const quoteUrl = requireCommandValue(findOption(args, "--quote-url"), "Usage: apitweet tweet quote --text <content> --quote-url <url>");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/tweets/quote",
      body: {
        ...buildTweetBody(args, state, config),
        quote_tweet_url: quoteUrl,
      },
    });
    return;
  }

  if (action === "lookup") {
    const tweetIds = collectPositionals(args, 2);
    if (tweetIds.length === 0) {
      exitWithError("Usage: apitweet tweet lookup <tweet_id...>");
    }
    const summary = args.includes("--summary");
    const result = await performRequest(state, config, {
      method: "POST",
      path: "/twitter/tweets/lookup",
      body: tweetIds,
      silent: summary,
    });

    if (summary && result.data && Array.isArray(result.data.data)) {
      for (const tweet of result.data.data) {
        console.log(`${tweet.tweet_id}:${tweet.is_paid_promotion}`);
      }
    }
    return;
  }

  if (action === "replies") {
    const tweetId = requireCommandValue(args[2], "Usage: apitweet tweet replies <tweet_id> [--count <n>] [--sort Relevance|Recency|Likes]");
    const count = readCountOption(args, 50);
    const sort = findOption(args, "--sort");
    const querySuffix = sort ? `?sort_by=${encodeURIComponent(sort)}` : "";
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/tweets/${encodeURIComponent(tweetId)}/replies/${count}${querySuffix}`,
    });
    return;
  }

  if (action === "like" || action === "unlike" || action === "bookmark" || action === "unbookmark" || action === "retweet" || action === "unretweet") {
    const tweetId = requireCommandValue(args[2], `Usage: apitweet tweet ${action} <tweet_id>`);
    const mapping = {
      like: { method: "POST", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/like` },
      unlike: { method: "DELETE", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/like` },
      bookmark: { method: "POST", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/bookmark` },
      unbookmark: { method: "DELETE", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/bookmark` },
      retweet: { method: "POST", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/retweet` },
      unretweet: { method: "DELETE", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/retweet` },
    };
    await performRequest(state, config, {
      ...mapping[action],
      body: tweetActionBody(args, state, config),
    });
    return;
  }

  exitWithError(
    "Unknown tweet command.",
    "Use: tweet create | tweet quote | tweet lookup | tweet replies | tweet like | tweet unlike | tweet bookmark | tweet unbookmark | tweet retweet | tweet unretweet",
  );
}

async function handleUserCommand(state, config, args) {
  const action = args[1];
  const username = requireCommandValue(args[2], "Usage: apitweet user follow <username> | user unfollow <username>");
  const proxy = findOption(args, "--proxy");

  if (action === "follow") {
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/user/follow",
      body: {
        username,
        cookie: resolveCookieArg(args, state, config),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  if (action === "unfollow") {
    await performRequest(state, config, {
      method: "DELETE",
      path: "/twitter/user/follow",
      body: {
        username,
        cookie: resolveCookieArg(args, state, config),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  exitWithError("Unknown user command.", "Use: user follow | user unfollow");
}

async function handleGenericRequest(state, config, args) {
  const requestPath = requireCommandValue(args[0], "Usage: apitweet <path>");
  await performRequest(state, config, {
    method: state.method,
    path: requestPath,
    body: state.data,
  });
}

export async function runCommand(state, config) {
  const [command] = state.commandArgs;

  if (!command) {
    return false;
  }

  if (command.startsWith("/") || /^https?:\/\//i.test(command)) {
    await handleGenericRequest(state, config, state.commandArgs);
    return true;
  }

  if (command === "config") {
    await handleConfigCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "auth") {
    await handleAuthCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "users") {
    await handleUsersCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "about") {
    await handleAboutCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "search") {
    await handleSearchCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "followers") {
    await handleFollowersCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "following") {
    await handleFollowingCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "list") {
    await handleListCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "tweet") {
    await handleTweetCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "user") {
    await handleUserCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "article") {
    await handleArticleCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "dm") {
    await handleDmCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "profile") {
    await handleProfileCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "timeline") {
    await handleTimelineCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "trending") {
    await handleTrendingCommand(state, config, state.commandArgs);
    return true;
  }

  exitWithError(`Unknown command: ${command}`, "Run apitweet --help for usage.");
}
