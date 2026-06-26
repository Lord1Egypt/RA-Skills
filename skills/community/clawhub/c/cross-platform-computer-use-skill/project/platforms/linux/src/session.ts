import type {
  AppGrant,
  ComputerUseSessionContext,
  CuGrantFlags,
  CuPermissionRequest,
  CuPermissionResponse,
  ScreenshotDims,
} from './vendor/computer-use-mcp/types.js'
import { DEFAULT_GRANT_FLAGS } from './vendor/computer-use-mcp/types.js'
import { checkComputerUseLock, tryAcquireComputerUseLock } from './computer-use/computerUseLock.js'

type State = {
  allowedApps: AppGrant[]
  grantFlags: CuGrantFlags
  hiddenDuringTurn: Set<string>
  clipboardStash?: string
  selectedDisplayId?: number
  displayPinnedByModel?: boolean
  displayResolvedForApps?: string
  lastScreenshotDims?: ScreenshotDims
}

function autoApprovePermission(req: CuPermissionRequest): CuPermissionResponse {
  const granted = req.apps
    .filter(app => app.resolved && !app.alreadyGranted)
    .map(app => ({
      bundleId: app.resolved!.bundleId,
      displayName: app.resolved!.displayName,
      grantedAt: Date.now(),
      tier: app.proposedTier,
    }))

  const denied = req.apps
    .filter(app => !app.resolved)
    .map(app => ({
      bundleId: app.requestedName,
      reason: 'not_installed' as const,
    }))

  return {
    granted,
    denied,
    flags: {
      ...DEFAULT_GRANT_FLAGS,
      ...req.requestedFlags,
    },
  }
}

export function createSessionContext(): ComputerUseSessionContext {
  const state: State = {
    allowedApps: [],
    grantFlags: { ...DEFAULT_GRANT_FLAGS },
    hiddenDuringTurn: new Set<string>(),
  }

  return {
    getAllowedApps: () => state.allowedApps,
    getGrantFlags: () => state.grantFlags,
    getUserDeniedBundleIds: () => [],
    getSelectedDisplayId: () => state.selectedDisplayId,
    getDisplayPinnedByModel: () => state.displayPinnedByModel ?? false,
    getDisplayResolvedForApps: () => state.displayResolvedForApps,
    getLastScreenshotDims: () => state.lastScreenshotDims,
    onPermissionRequest: async req => autoApprovePermission(req),
    onAllowedAppsChanged: (apps, flags) => {
      state.allowedApps = [...apps]
      state.grantFlags = flags
    },
    onAppsHidden: ids => {
      for (const id of ids) state.hiddenDuringTurn.add(id)
    },
    getClipboardStash: () => state.clipboardStash,
    onClipboardStashChanged: stash => {
      state.clipboardStash = stash
    },
    onResolvedDisplayUpdated: displayId => {
      state.selectedDisplayId = displayId
      state.displayPinnedByModel = false
    },
    onDisplayPinned: displayId => {
      state.selectedDisplayId = displayId
      state.displayPinnedByModel = displayId !== undefined
      if (displayId === undefined) state.displayResolvedForApps = undefined
    },
    onDisplayResolvedForApps: key => {
      state.displayResolvedForApps = key
    },
    onScreenshotCaptured: dims => {
      state.lastScreenshotDims = dims
    },
    checkCuLock: async () => {
      const result = await checkComputerUseLock()
      switch (result.kind) {
        case 'free':
          return { holder: undefined, isSelf: false }
        case 'held_by_self':
          return { holder: process.env.CODEX_THREAD_ID ?? `pid-${process.pid}`, isSelf: true }
        case 'blocked':
          return { holder: result.by, isSelf: false }
      }
    },
    acquireCuLock: async () => {
      const result = await tryAcquireComputerUseLock()
      if (result.kind === 'blocked') {
        throw new Error(`Computer use is locked by another session (${result.by}).`)
      }
    },
    formatLockHeldMessage: holder =>
      `Computer use is already in use by another session (${holder.slice(0, 8)}...).`,
  }
}
