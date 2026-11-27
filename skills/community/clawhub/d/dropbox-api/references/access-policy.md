# Dropbox access policy

An access policy limits which endpoints Dropbox connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/dropbox#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Dropbox: its 64 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create dropbox --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "POST", "path": "2/account/get_photo"},
    {"method": "POST", "path": "2/check/user"},
    {"method": "POST", "path": "2/file_properties/properties/search"},
    {"method": "POST", "path": "2/file_properties/properties/search/continue"},
    {"method": "POST", "path": "2/file_properties/templates/get_for_user"},
    {"method": "POST", "path": "2/file_properties/templates/list_for_user"},
    {"method": "POST", "path": "2/file_requests/count"},
    {"method": "POST", "path": "2/file_requests/get"},
    {"method": "POST", "path": "2/file_requests/list"},
    {"method": "POST", "path": "2/file_requests/list/continue"},
    {"method": "POST", "path": "2/file_requests/list_v2"},
    {"method": "POST", "path": "2/files/alpha/get_metadata"},
    {"method": "POST", "path": "2/files/download"},
    {"method": "POST", "path": "2/files/download_zip"},
    {"method": "POST", "path": "2/files/export"},
    {"method": "POST", "path": "2/files/get_file_lock_batch"},
    {"method": "POST", "path": "2/files/get_metadata"},
    {"method": "POST", "path": "2/files/get_preview"},
    {"method": "POST", "path": "2/files/get_temporary_link"},
    {"method": "POST", "path": "2/files/get_thumbnail"},
    {"method": "POST", "path": "2/files/get_thumbnail_batch"},
    {"method": "POST", "path": "2/files/get_thumbnail_v2"},
    {"method": "POST", "path": "2/files/list_folder"},
    {"method": "POST", "path": "2/files/list_folder/continue"},
    {"method": "POST", "path": "2/files/list_folder/get_latest_cursor"},
    {"method": "POST", "path": "2/files/list_revisions"},
    {"method": "POST", "path": "2/files/search"},
    {"method": "POST", "path": "2/files/search/continue_v2"},
    {"method": "POST", "path": "2/files/search_v2"},
    {"method": "POST", "path": "2/files/tags/get"},
    {"method": "POST", "path": "2/openid/userinfo"},
    {"method": "POST", "path": "2/paper/docs/download"},
    {"method": "POST", "path": "2/paper/docs/folder_users/list"},
    {"method": "POST", "path": "2/paper/docs/folder_users/list/continue"},
    {"method": "POST", "path": "2/paper/docs/get_folder_info"},
    {"method": "POST", "path": "2/paper/docs/get_metadata"},
    {"method": "POST", "path": "2/paper/docs/list"},
    {"method": "POST", "path": "2/paper/docs/list/continue"},
    {"method": "POST", "path": "2/paper/docs/sharing_policy/get"},
    {"method": "POST", "path": "2/paper/docs/users/list"},
    {"method": "POST", "path": "2/paper/docs/users/list/continue"},
    {"method": "POST", "path": "2/sharing/get_file_metadata"},
    {"method": "POST", "path": "2/sharing/get_file_metadata/batch"},
    {"method": "POST", "path": "2/sharing/get_folder_metadata"},
    {"method": "POST", "path": "2/sharing/get_shared_link_file"},
    {"method": "POST", "path": "2/sharing/get_shared_link_metadata"},
    {"method": "POST", "path": "2/sharing/get_shared_links"},
    {"method": "POST", "path": "2/sharing/list_file_members"},
    {"method": "POST", "path": "2/sharing/list_file_members/batch"},
    {"method": "POST", "path": "2/sharing/list_file_members/continue"},
    {"method": "POST", "path": "2/sharing/list_folder_members"},
    {"method": "POST", "path": "2/sharing/list_folder_members/continue"},
    {"method": "POST", "path": "2/sharing/list_folders"},
    {"method": "POST", "path": "2/sharing/list_folders/continue"},
    {"method": "POST", "path": "2/sharing/list_mountable_folders"},
    {"method": "POST", "path": "2/sharing/list_mountable_folders/continue"},
    {"method": "POST", "path": "2/sharing/list_received_files"},
    {"method": "POST", "path": "2/sharing/list_received_files/continue"},
    {"method": "POST", "path": "2/sharing/list_shared_links"},
    {"method": "POST", "path": "2/users/features/get_values"},
    {"method": "POST", "path": "2/users/get_account"},
    {"method": "POST", "path": "2/users/get_account_batch"},
    {"method": "POST", "path": "2/users/get_current_account"},
    {"method": "POST", "path": "2/users/get_space_usage"}
  ],
  "deny": []
}
```

## Endpoints

The Dropbox endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | 2/account/delete_profile_photo | write | account | Deletes the current user's profile photo. |
| POST | 2/account/get_photo | read | account | Gets the account photo of a given user. |
| POST | 2/account/set_profile_photo | write | account | Sets a user's profile photo. |
| POST | 2/auth/token/revoke | write | auth | Disables the access token used to authenticate the call. |
| POST | 2/check/user | read | check | This endpoint performs User Authentication, validating the supplied access token, and returns the supplied string, to allow you to test your code and connection to the Dropbox API. It has no other effect. |
| POST | 2/contacts/delete_manual_contacts | write | contacts | Removes all manually added contacts. |
| POST | 2/contacts/delete_manual_contacts_batch | write | contacts | Removes manually added contacts from the given list. |
| POST | 2/file_properties/properties/add | write | file_properties | Add property groups to a Dropbox file. |
| POST | 2/file_properties/properties/overwrite | write | file_properties | Overwrite property groups associated with a file. |
| POST | 2/file_properties/properties/remove | write | file_properties | Permanently removes the specified property group from the file. |
| POST | 2/file_properties/properties/search | read | file_properties | Search across property templates for particular property field values. |
| POST | 2/file_properties/properties/search/continue | read | file_properties | Once a cursor has been retrieved from properties/search, use this to paginate through all search results. |
| POST | 2/file_properties/properties/update | write | file_properties | Add, update or remove properties associated with the supplied file and templates. |
| POST | 2/file_properties/templates/add_for_user | write | file_properties | Add a template associated with a user. |
| POST | 2/file_properties/templates/get_for_user | read | file_properties | Get the schema for a specified template. |
| POST | 2/file_properties/templates/list_for_user | read | file_properties | Get the template identifiers for a team. |
| POST | 2/file_properties/templates/remove_for_user | write | file_properties | Permanently removes the specified template created from templates/add_for_user. |
| POST | 2/file_properties/templates/update_for_user | write | file_properties | Update a template associated with a user. |
| POST | 2/file_requests/count | read | file_requests | Returns the total number of file requests owned by this user. |
| POST | 2/file_requests/create | write | file_requests | Creates a file request for this user. |
| POST | 2/file_requests/delete | write | file_requests | Delete a batch of closed file requests. |
| POST | 2/file_requests/delete_all_closed | write | file_requests | Delete all closed file requests owned by this user. |
| POST | 2/file_requests/get | read | file_requests | Returns the specified file request. |
| POST | 2/file_requests/list | read | file_requests | Returns a list of file requests owned by this user. |
| POST | 2/file_requests/list/continue | read | file_requests | Once a cursor has been retrieved from list:2, use this to paginate through all file requests. |
| POST | 2/file_requests/list_v2 | read | file_requests | Returns a list of file requests owned by this user. |
| POST | 2/file_requests/update | write | file_requests | Update a file request. |
| POST | 2/files/alpha/get_metadata | read | files | Returns the metadata for a file or folder. |
| POST | 2/files/alpha/upload | write | files | Create a new file with the contents provided in the request. |
| POST | 2/files/copy | write | files | Copy a file or folder to a different location in the user's Dropbox. |
| POST | 2/files/copy_batch | write | files | Copy multiple files or folders to different locations at once in the user's Dropbox. |
| POST | 2/files/copy_batch/check | write | files | Returns the status of an asynchronous job for copy_batch:1. |
| POST | 2/files/copy_batch/check_v2 | write | files | Returns the status of an asynchronous job for copy_batch:2. |
| POST | 2/files/copy_batch_v2 | write | files | Copy multiple files or folders to different locations at once in the user's Dropbox. |
| POST | 2/files/copy_reference/get | write | files | Get a copy reference to a file or folder. |
| POST | 2/files/copy_reference/save | write | files | Save a copy reference returned by copy_reference/get to the user's Dropbox. |
| POST | 2/files/copy_v2 | write | files | Copy a file or folder to a different location in the user's Dropbox. |
| POST | 2/files/create_folder | write | files | Create a folder at a given path. |
| POST | 2/files/create_folder_batch | write | files | Create multiple folders at once. |
| POST | 2/files/create_folder_batch/check | write | files | Returns the status of an asynchronous job for create_folder_batch. |
| POST | 2/files/create_folder_v2 | write | files | Create a folder at a given path. |
| POST | 2/files/delete | write | files | Delete the file or folder at a given path. |
| POST | 2/files/delete_batch | write | files | Delete multiple files/folders at once. |
| POST | 2/files/delete_batch/check | write | files | Returns the status of an asynchronous job for delete_batch. |
| POST | 2/files/delete_v2 | write | files | Delete the file or folder at a given path. |
| POST | 2/files/download | read | files | Download a file from a user's Dropbox. |
| POST | 2/files/download_zip | read | files | Download a folder from the user's Dropbox, as a zip file. |
| POST | 2/files/export | read | files | Export a file from a user's Dropbox. |
| POST | 2/files/get_file_lock_batch | read | files | Return the lock metadata for the given list of paths. |
| POST | 2/files/get_metadata | read | files | Returns the metadata for a file or folder. |
| POST | 2/files/get_preview | read | files | Get a preview for a file. |
| POST | 2/files/get_temporary_link | read | files | Get a temporary link to stream content of a file. |
| POST | 2/files/get_temporary_upload_link | write | files | Get a one-time use temporary upload link to upload a file to a Dropbox location. |
| POST | 2/files/get_thumbnail | read | files | Get a thumbnail for an image. |
| POST | 2/files/get_thumbnail_batch | read | files | Get thumbnails for a list of images. |
| POST | 2/files/get_thumbnail_v2 | read | files | Get a thumbnail for an image. |
| POST | 2/files/list_folder | read | files | Starts returning the contents of a folder. |
| POST | 2/files/list_folder/continue | read | files | Once a cursor has been retrieved from list_folder, use this to paginate through all files and retrieve updates to the folder, following the same rules as documented for list_folder. |
| POST | 2/files/list_folder/get_latest_cursor | read | files | A way to quickly get a cursor for the folder's state. |
| POST | 2/files/list_revisions | read | files | Returns revisions for files based on a file path or a file id. |
| POST | 2/files/lock_file_batch | write | files | Lock the files at the given paths. |
| POST | 2/files/move | write | files | Move a file or folder to a different location in the user's Dropbox. |
| POST | 2/files/move_batch | write | files | Move multiple files or folders to different locations at once in the user's Dropbox. |
| POST | 2/files/move_batch/check | write | files | Returns the status of an asynchronous job for move_batch:1. |
| POST | 2/files/move_batch/check_v2 | write | files | Returns the status of an asynchronous job for move_batch:2. |
| POST | 2/files/move_batch_v2 | write | files | Move multiple files or folders to different locations at once in the user's Dropbox. |
| POST | 2/files/move_v2 | write | files | Move a file or folder to a different location in the user's Dropbox. |
| POST | 2/files/paper/create | write | files | Creates a new Paper doc with the provided content. |
| POST | 2/files/paper/update | write | files | Updates an existing Paper doc with the provided content. |
| POST | 2/files/permanently_delete | write | files | Permanently delete the file or folder at a given path (see https://www.dropbox.com/en/help/40). |
| POST | 2/files/properties/add | write | files | Add property groups to a Dropbox file. |
| POST | 2/files/properties/overwrite | write | files | Overwrite property groups associated with a file. |
| POST | 2/files/properties/update | write | files | Add, update or remove properties associated with the supplied file and templates. |
| POST | 2/files/restore | write | files | Restore a specific revision of a file to the given path. |
| POST | 2/files/save_url | write | files | Save the data from a specified URL into a file in user's Dropbox. |
| POST | 2/files/save_url/check_job_status | write | files | Check the status of a save_url job. |
| POST | 2/files/search | read | files | Searches for files and folders. |
| POST | 2/files/search/continue_v2 | read | files | Fetches the next page of search results returned from search:2. |
| POST | 2/files/search_v2 | read | files | Searches for files and folders. |
| POST | 2/files/tags/add | write | files | Add a tag to an item. |
| POST | 2/files/tags/get | read | files | Get list of tags assigned to items. |
| POST | 2/files/tags/remove | write | files | Remove a tag from an item. |
| POST | 2/files/unlock_file_batch | write | files | Unlock the files at the given paths. |
| POST | 2/files/upload | write | files | Create a new file with the contents provided in the request. |
| POST | 2/files/upload_session/append | write | files | Append more data to an upload session. |
| POST | 2/files/upload_session/append_batch | write | files | Append more data to multiple upload sessions. |
| POST | 2/files/upload_session/append_v2 | write | files | Append more data to an upload session. |
| POST | 2/files/upload_session/finish | write | files | Finish an upload session and save the uploaded data to the given file path. |
| POST | 2/files/upload_session/finish_batch | write | files | This route helps you commit many files at once into a user's Dropbox. |
| POST | 2/files/upload_session/finish_batch/check | write | files | Returns the status of an asynchronous job for upload_session/finish_batch. |
| POST | 2/files/upload_session/finish_batch_v2 | write | files | This route helps you commit many files at once into a user's Dropbox. |
| POST | 2/files/upload_session/start | write | files | Upload sessions allow you to upload a single file in one or more requests, for example where the size of the file is greater than 150 MiB. This call starts a new upload session with the given data. |
| POST | 2/files/upload_session/start_batch | write | files | Start a batch of upload sessions. |
| POST | 2/openid/userinfo | read | openid | This route is used for refreshing the info that is found in the id_token during the OIDC flow. |
| POST | 2/paper/docs/archive | write | paper | Marks the given Paper doc as archived. |
| POST | 2/paper/docs/create | write | paper | Creates a new Paper doc with the provided content. |
| POST | 2/paper/docs/download | read | paper | Exports and downloads Paper doc either as HTML or markdown. |
| POST | 2/paper/docs/folder_users/list | read | paper | Lists the users who are explicitly invited to the Paper folder in which the Paper doc is contained. |
| POST | 2/paper/docs/folder_users/list/continue | read | paper | Once a cursor has been retrieved from docs/folder_users/list, use this to paginate through all users on the Paper folder. |
| POST | 2/paper/docs/get_folder_info | read | paper | Retrieves folder information for the given Paper doc. |
| POST | 2/paper/docs/get_metadata | read | paper | Returns metadata for a Paper doc or Cloud Doc. |
| POST | 2/paper/docs/list | read | paper | Return the list of all Paper docs according to the argument specifications. |
| POST | 2/paper/docs/list/continue | read | paper | Once a cursor has been retrieved from docs/list, use this to paginate through all Paper doc. |
| POST | 2/paper/docs/permanently_delete | write | paper | Permanently deletes the given Paper doc. |
| POST | 2/paper/docs/sharing_policy/get | read | paper | Gets the default sharing policy for the given Paper doc. |
| POST | 2/paper/docs/sharing_policy/set | write | paper | Sets the default sharing policy for the given Paper doc. |
| POST | 2/paper/docs/update | write | paper | Updates an existing Paper doc with the provided content. |
| POST | 2/paper/docs/users/add | write | paper | Allows an owner or editor to add users to a Paper doc or change their permissions using their email address or Dropbox account ID. The doc owner's permissions cannot be changed. |
| POST | 2/paper/docs/users/list | read | paper | Lists all users who visited the Paper doc or users with explicit access. |
| POST | 2/paper/docs/users/list/continue | read | paper | Once a cursor has been retrieved from docs/users/list, use this to paginate through all users on the Paper doc. |
| POST | 2/paper/docs/users/remove | write | paper | Allows an owner or editor to remove users from a Paper doc using their email address or Dropbox account ID. The doc owner cannot be removed. |
| POST | 2/paper/folders/create | write | paper | Create a new Paper folder with the provided info. |
| POST | 2/sharing/add_file_member | write | sharing | Adds specified members to a file. |
| POST | 2/sharing/add_folder_member | write | sharing | Allows an owner or editor (if the ACL update policy allows) of a shared folder to add another member. |
| POST | 2/sharing/check_job_status | write | sharing | Returns the status of an asynchronous job. |
| POST | 2/sharing/check_remove_member_job_status | write | sharing | Returns the status of an asynchronous job for sharing a folder. |
| POST | 2/sharing/check_share_job_status | write | sharing | Returns the status of an asynchronous job for sharing a folder. |
| POST | 2/sharing/create_shared_link | write | sharing | Create a shared link. |
| POST | 2/sharing/create_shared_link_with_settings | write | sharing | Create a shared link with custom settings. |
| POST | 2/sharing/get_file_metadata | read | sharing | Returns shared file metadata. |
| POST | 2/sharing/get_file_metadata/batch | read | sharing | Returns shared file metadata. |
| POST | 2/sharing/get_folder_metadata | read | sharing | Returns shared folder metadata by its folder ID. |
| POST | 2/sharing/get_shared_link_file | read | sharing | Download the shared link's file from a user's Dropbox. |
| POST | 2/sharing/get_shared_link_metadata | read | sharing | Get the shared link's metadata. |
| POST | 2/sharing/get_shared_links | read | sharing | Get shared links of a path (deprecated; use list_shared_links). |
| POST | 2/sharing/list_file_members | read | sharing | Use to obtain the members who have been invited to a file, both inherited and uninherited members. |
| POST | 2/sharing/list_file_members/batch | read | sharing | Get members of multiple files at once. |
| POST | 2/sharing/list_file_members/continue | read | sharing | Once a cursor has been retrieved from list_file_members or list_file_members/batch, use this to paginate through all shared file members. |
| POST | 2/sharing/list_folder_members | read | sharing | Returns shared folder membership by its folder ID. |
| POST | 2/sharing/list_folder_members/continue | read | sharing | Once a cursor has been retrieved from list_folder_members, use this to paginate through all shared folder members. |
| POST | 2/sharing/list_folders | read | sharing | Return the list of all shared folders the current user has access to. |
| POST | 2/sharing/list_folders/continue | read | sharing | Once a cursor has been retrieved from list_folders, use this to paginate through all shared folders. |
| POST | 2/sharing/list_mountable_folders | read | sharing | Return the list of all shared folders the current user can mount or unmount. |
| POST | 2/sharing/list_mountable_folders/continue | read | sharing | Once a cursor has been retrieved from list_mountable_folders, use this to paginate through all mountable shared folders. |
| POST | 2/sharing/list_received_files | read | sharing | Returns a list of all files shared with current user. |
| POST | 2/sharing/list_received_files/continue | read | sharing | Get more results with a cursor from list_received_files. |
| POST | 2/sharing/list_shared_links | read | sharing | List shared links of this user. |
| POST | 2/sharing/modify_shared_link_settings | write | sharing | Modify the shared link's settings. |
| POST | 2/sharing/mount_folder | write | sharing | The current user mounts the designated folder. |
| POST | 2/sharing/relinquish_access | write | sharing | Removes all self-removable access from a file or folder for the current user. |
| POST | 2/sharing/relinquish_file_membership | write | sharing | The current user relinquishes their membership in the designated file. |
| POST | 2/sharing/relinquish_folder_membership | write | sharing | The current user relinquishes their membership in the designated shared folder and will no longer have access to the folder. |
| POST | 2/sharing/remove_file_member_2 | write | sharing | Removes a specified member from the file. |
| POST | 2/sharing/remove_folder_member | write | sharing | Allows an owner or editor (if the ACL update policy allows) of a shared folder to remove another member. |
| POST | 2/sharing/revoke_shared_link | write | sharing | Revoke a shared link. |
| POST | 2/sharing/set_access_inheritance | write | sharing | Change the inheritance policy of an existing Shared Folder. |
| POST | 2/sharing/share_folder | write | sharing | Share a folder with collaborators. |
| POST | 2/sharing/transfer_folder | write | sharing | Transfer ownership of a shared folder to a member of the shared folder. |
| POST | 2/sharing/unmount_folder | write | sharing | The current user unmounts the designated folder. |
| POST | 2/sharing/unshare_file | write | sharing | Remove all members from this file. |
| POST | 2/sharing/unshare_folder | write | sharing | Allows a shared folder owner to unshare the folder. |
| POST | 2/sharing/update_file_member | write | sharing | Changes a member's access on a shared file. |
| POST | 2/sharing/update_file_policy | write | sharing | Update the viewer info policy of a file. |
| POST | 2/sharing/update_folder_member | write | sharing | Allows an owner or editor of a shared folder to update another member's permissions. |
| POST | 2/sharing/update_folder_policy | write | sharing | Update the sharing policies for a shared folder. |
| POST | 2/users/features/get_values | read | users | Get a list of feature values that may be configured for the current account. |
| POST | 2/users/get_account | read | users | Get information about a user's account. |
| POST | 2/users/get_account_batch | read | users | Get information about multiple user accounts. |
| POST | 2/users/get_current_account | read | users | Get information about the current user's account. |
| POST | 2/users/get_space_usage | read | users | Get the space usage information for the current user's account. |
