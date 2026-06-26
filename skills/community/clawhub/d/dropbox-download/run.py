from typing import Annotated

def run(
    pipedream: Annotated[PipedreamAuth, Integration("dropbox")],
    path: Annotated[str, "The path of the file to download."],
    rev: Annotated[str | None, "Please specify revision in path instead."] = None,
):

    # Track initial props for reload comparison
    initial_props = {
          "dropbox", "path", "rev",
    }

    state_manager = PipedreamStateManager(pipedream, "Download File", initial_props, {})
    state_manager.add_prop("dropbox", {"authProvisionId": pipedream.auth_provision_id})

    state_manager.add_prop("path", path)

    rev_config = state_manager.resolve_prop("rev", rev, use_query=False, use_lv=False)
    state_manager.add_prop("rev", rev_config)

    return state_manager.run()
