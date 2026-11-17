const fs = require("fs");
const { URL } = require("url");
const path = require("path");
const http = require("http");
const https = require("https");
const { EventEmitter } = require("events");

const DOWNLOAD_STATES = {
  IDLE: "IDLE",
  SKIPPED: "SKIPPED",
  STARTED: "STARTED",
  DOWNLOADING: "DOWNLOADING",
  RETRY: "RETRY",
  PAUSED: "PAUSED",
  RESUMED: "RESUMED",
  STOPPED: "STOPPED",
  FINISHED: "FINISHED",
  FAILED: "FAILED",
};

/**
 * https://github.com/hgouveia/node-downloader-helper
 */
class Downloader extends EventEmitter {
  constructor(url, savePath, options = {}) {
    super({ captureRejections: true });

    if (!this.__validate(url, savePath)) {
      return;
    }

    this.url = this.requestURL = url.trim();
    this.state = DOWNLOAD_STATES.IDLE;
    this.__defaultOpts = {
      body: null,
      retry: false,
      method: "GET",
      headers: {},
      fileName: "",
      timeout: -1,
      metadata: null,
      override: false,
      forceResume: false,
      removeOnStop: true,
      removeOnFail: true,
      maxRedirects: 10,
      progressThrottle: 1000,
      httpRequestOptions: {},
      httpsRequestOptions: {},
      resumeOnIncomplete: true,
      resumeIfFileExists: false,
      resumeOnIncompleteMaxRetry: 5,
    };
    this.__opts = Object.assign({}, this.__defaultOpts);
    this.__pipes = [];
    this.__total = 0;
    this.__downloaded = 0;
    this.__progress = 0;
    this.__retryCount = 0;
    this.__retryTimeout = null;
    this.__resumeRetryCount = 0;
    this.__redirectCount = 0;
    this.__states = DOWNLOAD_STATES;
    this.__promise = null;
    this.__request = null;
    this.__response = null;
    this.__isAborted = false;
    this.__isResumed = false;
    this.__isResumable = false;
    this.__isRedirected = false;
    this.__destFolder = savePath;
    this.__statsEstimate = {
      time: 0,
      bytes: 0,
      prevBytes: 0,
      throttleTime: 0,
    };
    this.__fileName = "";
    this.__filePath = "";
    this.__defaultHttpAgent = new http.Agent({ keepAlive: false });
    this.__defaultHttpsAgent = new https.Agent({ keepAlive: false });
    this.updateOptions(options);
  }

  start() {
    const startPromise = () =>
      new Promise((resolve, reject) => {
        this.__promise = { resolve, reject };
        this.__start();
      });
    this.__redirectCount = 0;

    if (
      this.__opts.resumeIfFileExists &&
      this.state !== this.__states.RESUMED
    ) {
      return this.getTotalSize().then(({ name, total }) => {
        const override = this.__opts.override;
        this.__opts.override = true;
        this.__filePath = this.__getFilePath(name);
        this.__opts.override = override;
        if (this.__filePath && fs.existsSync(this.__filePath)) {
          const fileSize = this.__getFilesizeInBytes(this.__filePath);
          return fileSize !== total
            ? this.resumeFromFile(this.__filePath, { total, fileName: name })
            : startPromise();
        }
        return startPromise();
      });
    }
    return startPromise();
  }

  pause() {
    if (this.state === this.__states.STOPPED) {
      return Promise.resolve(true);
    }

    if (this.__response) {
      this.__response.unpipe();
      this.__pipes.forEach((pipe) => pipe.stream.unpipe());
    }

    if (this.__fileStream) {
      this.__fileStream.removeAllListeners();
    }

    this.__requestAbort();

    return this.__closeFileStream().then(() => {
      this.__setState(this.__states.PAUSED);
      this.emit("pause");
      return true;
    });
  }

  resume() {
    this.__redirectCount = 0;

    if (!this.__promise) {
      return this.start();
    }

    if (this.state === this.__states.STOPPED) {
      return Promise.resolve(false);
    }

    this.__setState(this.__states.RESUMED);
    if (this.__isResumable) {
      this.__isResumed = true;
      this.__reqOptions["headers"]["range"] = `bytes=${this.__downloaded}-`;
    }
    this.emit("resume", this.__isResumed);
    return this.__start();
  }

  stop() {
    if (this.state === this.__states.STOPPED) {
      return Promise.resolve(true);
    }
    const removeFile = () =>
      new Promise((resolve, reject) => {
        fs.access(this.__filePath, (_accessErr) => {
          if (_accessErr) {
            this.__emitStop();
            return resolve(true);
          }

          fs.unlink(this.__filePath, (_err) => {
            if (_err) {
              this.__setState(this.__states.FAILED);
              this.emit("error", _err);
              return reject(_err);
            }
            this.__emitStop();
            resolve(true);
          });
        });
      });

    this.__requestAbort();

    return this.__closeFileStream().then(() => {
      if (this.__opts.removeOnStop) {
        return removeFile();
      }
      this.__emitStop();
      return Promise.resolve(true);
    });
  }

  pipe(stream, options = null) {
    this.__pipes.push({ stream, options });
    return stream;
  }

  unpipe(stream = null) {
    const unpipeStream = (_stream) =>
      this.__response ? this.__response.unpipe(_stream) : _stream.unpipe();

    if (stream) {
      const pipe = this.__pipes.find((p) => p.stream === stream);
      if (pipe) {
        unpipeStream(stream);
        this.__pipes = this.__pipes.filter((p) => p.stream !== stream);
      }
      return;
    }

    this.__pipes.forEach((p) => unpipeStream(p.stream));
    this.__pipes = [];
  }

  getDownloadPath() {
    return this.__filePath;
  }

  isResumable() {
    return this.__isResumable;
  }

  updateOptions(options, url = "") {
    this.__opts = Object.assign({}, this.__opts, options);
    this.__headers = this.__opts.headers;

    if (this.__opts.timeout > -1) {
      this.__opts.httpRequestOptions.timeout = this.__opts.timeout;
      this.__opts.httpsRequestOptions.timeout = this.__opts.timeout;
    }

    if (
      typeof this.__opts.progressThrottle !== "number" ||
      this.__opts.progressThrottle < 0
    ) {
      this.__opts.progressThrottle = this.__defaultOpts.progressThrottle;
    }

    this.url = url || this.url;
    this.__reqOptions = this.__getReqOptions(
      this.__opts.method,
      this.url,
      this.__opts.headers,
    );
    this.__initProtocol(this.url);
  }

  getOptions() {
    return this.__opts;
  }

  getMetadata() {
    return this.__opts.metadata;
  }

  getStats() {
    return {
      total: this.__total,
      name: this.__fileName,
      downloaded: this.__downloaded,
      progress: this.__progress,
      speed: this.__statsEstimate.bytes,
    };
  }

  getTotalSize() {
    return new Promise((resolve, reject) => {
      const getReqOptions = (url) => {
        this.__initProtocol(url);
        const headers = Object.assign({}, this.__headers);
        if (headers.hasOwnProperty("range")) {
          delete headers["range"];
        }
        const reqOptions = this.__getReqOptions("HEAD", url, headers);
        return Object.assign({}, this.__reqOptions, reqOptions);
      };

      let retryCount = 0;
      let retryTimeout = null;
      let redirectCount = 0;

      const retry = (err, url) => {
        if (!this.__opts.retry || typeof this.__opts.retry !== "object") {
          return Promise.reject(err || new Error("wrong retry options"));
        }

        if (retryTimeout) {
          clearTimeout(retryTimeout);
          retryTimeout = null;
        }

        const { delay: retryDelay = 0, maxRetries = 999 } = this.__opts.retry;

        if (retryCount >= maxRetries) {
          return Promise.reject(
            err || new Error("reached the maximum retries"),
          );
        }

        retryCount++;
        this.__setState(this.__states.RETRY);
        this.emit("retry", retryCount, this.__opts.retry, err);

        return new Promise((resolveRetry) => {
          retryTimeout = setTimeout(() => {
            this.__setState(this.__states.IDLE);
            getRequest(url, getReqOptions(url));
            resolveRetry();
          }, retryDelay);
        });
      };

      const getRequest = (url, options) => {
        if (retryTimeout) {
          clearTimeout(retryTimeout);
          retryTimeout = null;
        }
        const req = this.__protocol.request(options, (response) => {
          if (this.__isRequireRedirect(response)) {
            redirectCount++;
            if (redirectCount > this.__opts.maxRedirects) {
              const err = new Error("Too many redirects");
              this.__setState(this.__states.FAILED);
              this.emit("error", err);
              return reject(err);
            }

            const redirectedURL = /^https?:\/\//.test(response.headers.location)
              ? response.headers.location
              : new URL(response.headers.location, url).href;
            this.emit("redirected", redirectedURL, url);
            return getRequest(redirectedURL, getReqOptions(redirectedURL));
          }
          if (response.statusCode < 200 || response.statusCode >= 400) {
            const err = new Error(`Response status was ${response.statusCode}`);
            if (
              this.__opts.retry &&
              response.statusCode >= 500 &&
              response.statusCode < 600
            ) {
              return retry(err, url).catch(reject);
            }
            return reject(err);
          }
          resolve({
            name: this.__getFileNameFromHeaders(response.headers, response),
            total: parseInt(response.headers["content-length"]) || null,
          });
        });

        req.on("error", (err) => {
          if (this.__opts.retry) {
            return retry(err, url).catch(reject);
          }
          reject(err);
        });

        req.on("timeout", () => {
          if (this.__opts.retry) {
            return retry(new Error("timeout"), url).catch(reject);
          }
          reject(new Error("timeout"));
        });

        req.on("uncaughtException", (err) => {
          if (this.__opts.retry) {
            return retry(err, url).catch(reject);
          }
          reject(err);
        });

        req.end();
      };
      getRequest(this.url, getReqOptions(this.url));
    });
  }

  getResumeState() {
    return {
      downloaded: this.__downloaded,
      filePath: this.__filePath,
      fileName: this.__fileName,
      total: this.__total,
    };
  }

  resumeFromFile(filePath, state = {}) {
    this.__opts.override = true;
    this.__filePath = filePath;
    return (
      state.total && state.fileName
        ? Promise.resolve({ name: state.fileName, total: state.total })
        : this.getTotalSize()
    ).then(({ name, total }) => {
      this.__total = state.total || total;
      this.__fileName = state.fileName || name;
      this.__downloaded =
        state.downloaded || this.__getFilesizeInBytes(this.__filePath);
      this.__reqOptions["headers"]["range"] = `bytes=${this.__downloaded}-`;
      this.__isResumed = true;
      this.__isResumable = true;
      this.__setState(this.__states.RESUMED);
      this.emit("resume", this.__isResumed);
      return new Promise((resolve, reject) => {
        this.__promise = { resolve, reject };
        this.__start();
      });
    });
  }

  __start() {
    if (!this.__isRedirected && this.state !== this.__states.RESUMED) {
      this.emit("start");
      this.__setState(this.__states.STARTED);
      this.__initProtocol(this.url);
    }

    this.__response = null;
    this.__isAborted = false;

    if (this.__request && !this.__request.destroyed) {
      this.__request.destroy();
    }

    if (this.__retryTimeout) {
      clearTimeout(this.__retryTimeout);
      this.__retryTimeout = null;
    }

    this.__request = this.__downloadRequest(
      this.__promise.resolve,
      this.__promise.reject,
    );

    this.__request.on(
      "error",
      this.__onError(this.__promise.resolve, this.__promise.reject),
    );
    this.__request.on(
      "timeout",
      this.__onTimeout(this.__promise.resolve, this.__promise.reject),
    );
    this.__request.on(
      "uncaughtException",
      this.__onError(this.__promise.resolve, this.__promise.reject, true),
    );

    if (this.__opts.body) {
      this.__request.write(this.__opts.body);
    }

    this.__request.end();
  }

  __resolvePending() {
    if (!this.__promise) {
      return;
    }
    const { resolve } = this.__promise;
    this.__promise = null;
    return resolve(true);
  }

  __downloadRequest(resolve, reject) {
    return this.__protocol.request(this.__reqOptions, (response) => {
      this.__response = response;

      if (!this.__isResumed) {
        this.__total = parseInt(response.headers["content-length"]) || null;
        this.__resetStats();
      }

      if (this.__isResumed && response.statusCode === 200) {
        this.__isResumed = false;
        this.__total = parseInt(response.headers["content-length"]) || null;
        this.__resetStats();
      }

      if (this.__isRequireRedirect(response)) {
        this.__redirectCount++;
        if (this.__redirectCount > this.__opts.maxRedirects) {
          const err = new Error("Too many redirects");
          this.__setState(this.__states.FAILED);
          this.emit("error", err);
          return reject(err);
        }

        const redirectedURL = /^https?:\/\//.test(response.headers.location)
          ? response.headers.location
          : new URL(response.headers.location, this.url).href;
        this.__isRedirected = true;
        this.__initProtocol(redirectedURL);
        this.emit("redirected", redirectedURL, this.url);
        return this.__start();
      }

      if (response.statusCode < 200 || response.statusCode >= 400) {
        const err = new Error(`Response status was ${response.statusCode}`);
        err.status = response.statusCode || 0;
        err.body = response.body || "";

        if (response.statusCode >= 500 && response.statusCode < 600) {
          return this.__onError(resolve, reject)(err);
        }
        this.__setState(this.__states.FAILED);
        this.emit("error", err);
        return reject(err);
      }

      if (this.__opts.forceResume) {
        this.__isResumable = true;
      } else if (
        response.headers.hasOwnProperty("accept-ranges") &&
        response.headers["accept-ranges"] !== "none"
      ) {
        this.__isResumable = true;
      }

      this.__startDownload(response, resolve, reject);
    });
  }

  __startDownload(response, resolve, reject) {
    let readable = response;

    if (!this.__isResumed) {
      const _fileName = this.__getFileNameFromHeaders(response.headers);
      this.__filePath = this.__getFilePath(_fileName);
      this.__fileName = this.__filePath.split(path.sep).pop();
      if (fs.existsSync(this.__filePath)) {
        const downloadedSize = this.__getFilesizeInBytes(this.__filePath);
        const totalSize = this.__total ? this.__total : 0;
        if (
          typeof this.__opts.override === "object" &&
          this.__opts.override.skip &&
          (this.__opts.override.skipSmaller || downloadedSize >= totalSize)
        ) {
          this.emit("skip", {
            totalSize: this.__total,
            fileName: this.__fileName,
            filePath: this.__filePath,
            downloadedSize: downloadedSize,
          });
          this.__setState(this.__states.SKIPPED);
          return resolve(true);
        }
      }
      this.__fileStream = fs.createWriteStream(this.__filePath, {});
    } else {
      this.__fileStream = fs.createWriteStream(this.__filePath, { flags: "a" });
    }

    this.emit("download", {
      fileName: this.__fileName,
      filePath: this.__filePath,
      totalSize: this.__total,
      isResumed: this.__isResumed,
      downloadedSize: this.__downloaded,
    });
    this.__retryCount = 0;
    this.__isResumed = false;
    this.__isRedirected = false;
    this.__setState(this.__states.DOWNLOADING);
    this.__statsEstimate.time = new Date();
    this.__statsEstimate.throttleTime = new Date();

    readable.on("data", (chunk) => this.__calculateStats(chunk.length));
    this.__pipes.forEach((pipe) => {
      readable.pipe(pipe.stream, pipe.options);
      readable = pipe.stream;
    });
    readable.pipe(this.__fileStream);
    readable.on("error", this.__onError(resolve, reject));

    this.__fileStream.on("finish", this.__onFinished(resolve, reject));
    this.__fileStream.on("error", this.__onError(resolve, reject));
  }

  __hasFinished() {
    return (
      !this.__isAborted &&
      [
        this.__states.PAUSED,
        this.__states.STOPPED,
        this.__states.RETRY,
        this.__states.FAILED,
        this.__states.RESUMED,
      ].indexOf(this.state) === -1
    );
  }

  __isRequireRedirect(response) {
    const redirectCodes = [301, 302, 303, 307, 308];
    return (
      redirectCodes.includes(response.statusCode) &&
      response.headers.hasOwnProperty("location") &&
      response.headers.location
    );
  }

  __onFinished(resolve, reject) {
    return () => {
      this.__fileStream.close((_err) => {
        if (_err) {
          return reject(_err);
        }
        if (this.__hasFinished()) {
          const isIncomplete = !this.__total
            ? false
            : this.__downloaded !== this.__total;

          if (
            isIncomplete &&
            this.__isResumable &&
            this.__opts.resumeOnIncomplete &&
            this.__resumeRetryCount <= this.__opts.resumeOnIncompleteMaxRetry
          ) {
            this.__resumeRetryCount++;
            this.emit("warning", new Error("incomplete download, retrying"));
            return this.resume();
          }

          this.__setState(this.__states.FINISHED);
          this.__pipes = [];
          this.emit("end", {
            fileName: this.__fileName,
            filePath: this.__filePath,
            totalSize: this.__total,
            incomplete: isIncomplete,
            onDiskSize: this.__getFilesizeInBytes(this.__filePath),
            downloadedSize: this.__downloaded,
          });
        }
        return resolve(this.__downloaded === this.__total);
      });
    };
  }

  __closeFileStream() {
    if (!this.__fileStream) {
      return Promise.resolve(true);
    }
    return new Promise((resolve, reject) => {
      this.__fileStream.close((err) => {
        if (err) {
          return reject(err);
        }
        return resolve(true);
      });
    });
  }

  __onError(resolve, reject, abortReq = false) {
    return (err) => {
      this.__pipes = [];

      if (abortReq) {
        this.__requestAbort();
      }

      if (
        this.state === this.__states.STOPPED ||
        this.state === this.__states.FAILED
      ) {
        return;
      }
      if (!this.__opts.retry) {
        return this.__removeFile().finally(() => {
          this.__setState(this.__states.FAILED);
          this.emit("error", err);
          reject(err);
        });
      }
      return this.__retry(err).catch((_err) => {
        this.__removeFile().finally(() => {
          this.__setState(this.__states.FAILED);
          this.emit("error", _err ? _err : err);
          reject(_err ? _err : err);
        });
      });
    };
  }

  __retry(err = null) {
    if (!this.__opts.retry || typeof this.__opts.retry !== "object") {
      return Promise.reject(err || new Error("wrong retry options"));
    }

    const { delay: retryDelay = 0, maxRetries = 999 } = this.__opts.retry;

    if (this.__retryCount >= maxRetries) {
      return Promise.reject(err || new Error("reached the maximum retries"));
    }

    this.__retryCount++;
    this.__setState(this.__states.RETRY);
    this.emit("retry", this.__retryCount, this.__opts.retry, err);

    if (this.__response) {
      this.__response.unpipe();
      this.__pipes.forEach((pipe) => pipe.stream.unpipe());
    }

    if (this.__fileStream) {
      this.__fileStream.removeAllListeners();
    }

    this.__requestAbort();

    return this.__closeFileStream().then(
      () =>
        new Promise(
          (resolve) =>
            (this.__retryTimeout = setTimeout(
              () =>
                resolve(this.__downloaded > 0 ? this.resume() : this.__start()),
              retryDelay,
            )),
        ),
    );
  }

  __onTimeout(resolve, reject) {
    return () => {
      this.__requestAbort();

      if (!this.__opts.retry) {
        return this.__removeFile().finally(() => {
          this.__setState(this.__states.FAILED);
          this.emit("timeout");
          reject(new Error("timeout"));
        });
      }

      return this.__retry(new Error("timeout")).catch((_err) => {
        this.__removeFile().finally(() => {
          this.__setState(this.__states.FAILED);
          if (_err) {
            reject(_err);
          } else {
            this.emit("timeout");
            reject(new Error("timeout"));
          }
        });
      });
    };
  }

  __resetStats() {
    this.__retryCount = 0;
    this.__downloaded = 0;
    this.__progress = 0;
    this.__resumeRetryCount = 0;
    this.__statsEstimate = {
      time: 0,
      bytes: 0,
      prevBytes: 0,
      throttleTime: 0,
    };
  }

  __getFileNameFromHeaders(headers, response) {
    let fileName = "";

    const fileNameAndEncodingRegExp =
      /.*filename\*=.*?'.*?'([^"].+?[^"])(?:(?:;)|$)/i;
    const fileNameWithQuotesRegExp = /.*filename="(.*?)";?/i;
    const fileNameWithoutQuotesRegExp = /.*filename=([^"].+?[^"])(?:(?:;)|$)/i;

    const ContentDispositionHeaderExists = headers.hasOwnProperty(
      "content-disposition",
    );
    const fileNameAndEncodingMatch = !ContentDispositionHeaderExists
      ? null
      : headers["content-disposition"].match(fileNameAndEncodingRegExp);
    const fileNameWithQuotesMatch =
      !ContentDispositionHeaderExists || fileNameAndEncodingMatch
        ? null
        : headers["content-disposition"].match(fileNameWithQuotesRegExp);
    const fileNameWithoutQuotesMatch =
      !ContentDispositionHeaderExists ||
      fileNameAndEncodingMatch ||
      fileNameWithQuotesMatch
        ? null
        : headers["content-disposition"].match(fileNameWithoutQuotesRegExp);

    if (
      ContentDispositionHeaderExists &&
      (fileNameAndEncodingMatch ||
        fileNameWithQuotesMatch ||
        fileNameWithoutQuotesMatch)
    ) {
      fileName = headers["content-disposition"];
      fileName = fileName.trim();

      if (fileNameAndEncodingMatch) {
        fileName = fileNameAndEncodingMatch[1];
      } else if (fileNameWithQuotesMatch) {
        fileName = fileNameWithQuotesMatch[1];
      } else if (fileNameWithoutQuotesMatch) {
        fileName = fileNameWithoutQuotesMatch[1];
      }

      fileName = fileName.replace(/[/\\]/g, "");
    } else {
      const parsedURL = new URL(this.requestURL);
      const baseName = path.basename(parsedURL.pathname);
      fileName = baseName.length > 0 ? baseName : `${parsedURL.hostname}.html`;
    }

    return this.__opts.fileName
      ? this.__getFileNameFromOpts(fileName, response)
      : fileName.replace(/\.*$/, "");
  }

  __getFilePath(fileName) {
    const currentPath = path.join(this.__destFolder, fileName);
    let filePath = currentPath;

    if (!this.__opts.override && this.state !== this.__states.RESUMED) {
      filePath = this.__uniqFileNameSync(filePath);

      if (currentPath !== filePath) {
        this.emit("renamed", {
          path: filePath,
          fileName: filePath.split(path.sep).pop(),
          prevPath: currentPath,
          prevFileName: currentPath.split(path.sep).pop(),
        });
      }
    }

    return filePath;
  }

  __getFileNameFromOpts(fileName, response) {
    if (!this.__opts.fileName) {
      return fileName;
    } else if (typeof this.__opts.fileName === "string") {
      return this.__opts.fileName;
    } else if (typeof this.__opts.fileName === "function") {
      const currentPath = path.join(this.__destFolder, fileName);
      if (
        (response && response.headers) ||
        (this.__response && this.__response.headers)
      ) {
        return this.__opts.fileName(
          fileName,
          currentPath,
          (response ? response : this.__response).headers["content-type"],
        );
      } else {
        return this.__opts.fileName(fileName, currentPath);
      }
    } else if (typeof this.__opts.fileName === "object") {
      const fileNameOpts = this.__opts.fileName;
      const name = fileNameOpts.name;
      const ext = fileNameOpts.hasOwnProperty("ext") ? fileNameOpts.ext : false;

      if (typeof ext === "string") {
        return `${name}.${ext}`;
      } else if (typeof ext === "boolean") {
        if (ext) {
          return name;
        } else {
          const _ext = fileName.includes(".") ? fileName.split(".").pop() : "";
          return _ext !== "" ? `${name}.${_ext}` : name;
        }
      }
    }

    return fileName;
  }

  __calculateStats(receivedBytes) {
    const currentTime = new Date();
    const elapsedTime = currentTime - this.__statsEstimate.time;
    const throttleElapseTime = currentTime - this.__statsEstimate.throttleTime;
    const total = this.__total || 0;

    if (!receivedBytes) {
      return;
    }

    this.__downloaded += receivedBytes;
    this.__progress = total === 0 ? 0 : (this.__downloaded / total) * 100;

    if (this.__downloaded === total || elapsedTime > 1000) {
      this.__statsEstimate.time = currentTime;
      this.__statsEstimate.bytes =
        this.__downloaded - this.__statsEstimate.prevBytes;
      this.__statsEstimate.prevBytes = this.__downloaded;
    }

    if (
      this.__downloaded === total ||
      throttleElapseTime > this.__opts.progressThrottle
    ) {
      this.__statsEstimate.throttleTime = currentTime;
      this.emit("progress.throttled", this.getStats());
    }

    this.emit("progress", this.getStats());
  }

  __setState(state) {
    this.state = state;
    this.emit("stateChanged", this.state);
  }

  __getReqOptions(method, url, headers = {}) {
    const urlParse = new URL(url);
    const options = {
      protocol: urlParse.protocol,
      host: urlParse.hostname,
      port: urlParse.port,
      path: urlParse.pathname + urlParse.search,
      method,
    };

    if (urlParse.username || urlParse.password) {
      options.auth = `${urlParse.username}:${urlParse.password}`;
    }

    if (headers) {
      options["headers"] = headers;
    }

    return options;
  }

  __getFilesizeInBytes(filePath) {
    try {
      const stats = fs.statSync(filePath, { throwIfNoEntry: false });
      const fileSizeInBytes = stats.size || 0;
      return fileSizeInBytes;
    } catch (err) {
      this.emit("warning", err);
    }
    return 0;
  }

  __validate(url, savePath) {
    if (typeof url !== "string") {
      throw new Error("url should be a string");
    }

    if (url.trim() === "") {
      throw new Error("url couldn't be empty");
    }

    if (typeof savePath !== "string") {
      throw new Error("savePath should be a string");
    }

    if (savePath.trim() === "") {
      throw new Error("savePath couldn't be empty");
    }

    if (!fs.existsSync(savePath)) {
      throw new Error("savePath must exist");
    }

    const stats = fs.statSync(savePath);
    if (!stats.isDirectory()) {
      throw new Error("savePath must be a directory");
    }

    try {
      fs.accessSync(savePath, fs.constants.F_OK);
    } catch (error) {
      throw new Error("savePath must be writable");
    }

    return true;
  }

  __initProtocol(url) {
    const defaultOpts = this.__getReqOptions(
      this.__opts.method,
      url,
      this.__headers,
    );
    this.requestURL = url;

    if (url.indexOf("https://") > -1) {
      this.__protocol = https;
      defaultOpts.agent = this.__defaultHttpsAgent;
      this.__reqOptions = Object.assign(
        {},
        defaultOpts,
        this.__opts.httpsRequestOptions,
      );
    } else {
      this.__protocol = http;
      defaultOpts.agent = this.__defaultHttpAgent;
      this.__reqOptions = Object.assign(
        {},
        defaultOpts,
        this.__opts.httpRequestOptions,
      );
    }
  }

  __uniqFileNameSync(_path) {
    if (typeof _path !== "string" || _path === "") {
      return _path;
    }

    try {
      fs.accessSync(_path, fs.constants.F_OK);
      const pathInfo = _path.match(/(.*)(\([0-9]+\))(\..*)$/);
      let base, ext, suffix;

      if (pathInfo) {
        base = pathInfo[1].trim();
        ext = pathInfo[3];
        suffix = parseInt(pathInfo[2].replace(/\(|\)/g, ""));
      } else {
        const lastSlashIndex = _path.lastIndexOf(path.sep);
        const fileNameStart = lastSlashIndex + 1;
        const fileName = _path.substring(fileNameStart);
        const firstDotIndex = fileName.indexOf(".");

        ext = firstDotIndex > 0 ? fileName.substring(firstDotIndex) : "";
        base =
          firstDotIndex > 0
            ? _path.substring(0, fileNameStart + firstDotIndex)
            : _path;
        suffix = 0;
      }

      return this.__uniqFileNameSync(base + " (" + ++suffix + ")" + ext);
    } catch (_err) {
      return _path;
    }
  }

  __removeFile() {
    return new Promise((resolve) => {
      if (!this.__fileStream) {
        return resolve();
      }
      this.__fileStream.close((err) => {
        if (err) {
          this.emit("warning", err);
        }
        if (this.__opts.removeOnFail) {
          return fs.access(this.__filePath, (_accessErr) => {
            if (_accessErr) {
              return resolve();
            }

            fs.unlink(this.__filePath, (_err) => {
              if (_err) {
                this.emit("warning", _err);
              }
              resolve();
            });
          });
        }
        resolve();
      });
    });
  }

  __requestAbort() {
    this.__isAborted = true;
    if (this.__retryTimeout) {
      clearTimeout(this.__retryTimeout);
      this.__retryTimeout = null;
    }

    if (this.__response) {
      this.__response.destroy();
    }

    if (this.__request) {
      if (this.__request.destroy) {
        this.__request.destroy();
      } else {
        this.__request.abort();
      }
    }
  }

  __emitStop() {
    this.__resolvePending();
    this.__setState(this.__states.STOPPED);
    this.emit("stop");
  }
}

module.exports = { Downloader, DOWNLOAD_STATES };
