export const DEFAULT_CONFIG_PATH = '.cairn/config.json';
export const USAGE = `cairn — local hybrid index

Usage:
  cairn add <url|path> [--label <label>] [--include <ext> ...] [--exclude <substr> ...] [--force]
  cairn list [--kind <web|code|file|text|pdf>]
  cairn search "<query>" [-k <n>] [--kind <kind>] [--source <id|uri>] [--tag <tag>]
  cairn ask    "<query>" [-k <n>] [--kind <kind>] [--source <id|uri>] [--tag <tag>] [--entities <n>] [--edges <n>]
  cairn graph "<query>" [-k <n>] [--tag <tag>]
  cairn graph --entity <id>
  cairn path <from-id> <to-id> [--depth <n>] [--directed]
  cairn tags
  cairn refresh <id|uri|all>
  cairn reindex <id|uri|all>
  cairn link <from-id|uri> <to-id|uri>
  cairn unlink <from-id|uri> <to-id|uri>
  cairn links
  cairn remove <id|uri>
  cairn init`;
