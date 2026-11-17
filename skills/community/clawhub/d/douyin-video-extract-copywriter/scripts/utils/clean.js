const constants = require("../config/constants");
const helper = require("../utils/helper");
const utils = require("../utils/utils");
const fs = require("fs");
const path = require("path");
const { downloadPath } = utils;

/**
 * 清理技能运行中临时下载的过期文件，以节省磁盘空间
 */
function deleteExpire() {
  const now = Date.now();
  const filepath = downloadPath();

  fs.readdir(filepath, (err, files) => {
    if (err) {
      return;
    }
    files.forEach((file) => {
      fs.stat(path.join(filepath, file), (err, stats) => {
        if (err) {
          return;
        }
        const fileTime = stats.mtime || stats.birthtime;
        if (fileTime) {
          const fileDate = new Date(Date.parse(fileTime));
          if (fileDate.getTime() < now - constants.EXPIRE_TIME * 1000) {
            utils.printInfo(
              "清理技能运行中临时下载的过期文件: " + file + " ，以节省磁盘空间",
            );
            fs.unlink(path.join(filepath, file), (err) => {
              if (err) {
                utils.printError(
                  "删除过期文件失败: " + (err.message || String(err)),
                );
              }
            });
          }
        } else {
          utils.printError(
            "获取文件时间属性失败，本技能运行过程中会下载视频文件，可能占用磁盘空间，建议手动删除，文件路径: " +
              filepath,
          );
        }
      });
    });
  });
}

module.exports = {
  deleteExpire,
};
